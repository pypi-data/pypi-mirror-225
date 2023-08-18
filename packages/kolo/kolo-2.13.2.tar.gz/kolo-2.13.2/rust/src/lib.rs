#[cfg(not(PyPy))]
#[path = ""]
mod _kolo {
    use bstr::Finder;
    use once_cell::sync::Lazy;
    use pyo3::exceptions::PyAttributeError;
    use pyo3::exceptions::PyKeyError;
    use pyo3::exceptions::PyTypeError;
    use pyo3::exceptions::PyValueError;
    use pyo3::ffi;
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;
    use pyo3::types::PyFrame;
    use pyo3::types::PyList;
    use pyo3::types::PyTuple;
    use pyo3::types::PyType;
    use pyo3::AsPyPointer;
    use serde_json::json;
    use std::cell::RefCell;
    use std::collections::HashMap;
    use std::env::current_dir;
    use std::os::raw::c_int;
    use std::path::Path;
    use std::ptr;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::Mutex;
    use std::time::SystemTime;
    use thread_local::ThreadLocal;
    use ulid::Ulid;

    macro_rules! count {
        // Macro magic to find the length of $path
        // https://youtu.be/q6paRBbLgNw?t=4380
        ($($element:expr),*) => {
            [$(count![@SUBSTR; $element]),*].len()
        };
        (@SUBSTR; $_element:expr) => {()};
    }

    macro_rules! finder {
        ($name:ident = $path:expr) => {
            static $name: Lazy<Finder> = Lazy::new(|| Finder::new($path));
        };
        (pub $name:ident = $path:expr) => {
            pub static $name: Lazy<Finder> = Lazy::new(|| Finder::new($path));
        };
        (pub $name:ident = $($path:expr),+ $(,)?) => {
            pub static $name: Lazy<[Finder; count!($($path),*)]> = Lazy::new(|| {
                [
                    $(Finder::new($path),)+
                ]
            });
        };

    }

    finder!(CELERY_FINDER = "celery");
    finder!(SENTRY_FINDER = "sentry_sdk");
    finder!(DJANGO_FINDER = "django");
    finder!(FROZEN_FINDER = "<frozen ");
    finder!(EXEC_FINDER = "<string>");

    #[cfg(target_os = "windows")]
    mod windows {
        use bstr::Finder;
        use once_cell::sync::Lazy;
        finder!(pub MIDDLEWARE_FINDER = "\\kolo\\middleware.py");
        finder!(pub DJANGO_SETUP_FINDER = "django\\__init__.py");
        finder!(pub TEMPLATE_FINDER = "django\\template\\backends\\django.py");
        finder!(pub HUEY_FINDER = "\\huey\\api.py");
        finder!(pub REQUESTS_FINDER = "requests\\sessions");
        finder!(pub HTTPX_FINDER = "httpx\\_client.py");
        finder!(pub URLLIB_FINDER = "urllib\\request");
        finder!(pub URLLIB3_FINDER = "urllib3\\connectionpool");
        finder!(pub LOGGING_FINDER = "\\logging\\");
        finder!(pub SQL_FINDER = "\\django\\db\\models\\sql\\compiler.py");
        finder!(pub PYTEST_FINDER = "kolo\\pytest_plugin.py");
        finder!(pub UNITTEST_FINDER = "unittest\\result.py");
        finder!(pub LIBRARY_FINDERS = "lib\\python", "\\site-packages\\", "\\x64\\lib\\");
        finder!(pub LOWER_PYTHON_FINDER = "\\python\\");
        finder!(pub UPPER_PYTHON_FINDER = "\\Python\\");
        finder!(pub LOWER_LIB_FINDER = "\\lib\\");
        finder!(pub UPPER_LIB_FINDER = "\\Lib\\");
        finder!(pub KOLO_FINDERS = "\\kolo\\middleware", "\\kolo\\profiler", "\\kolo\\serialize", "\\kolo\\pytest_plugin.py");
    }
    #[cfg(target_os = "windows")]
    use windows::*;

    #[cfg(not(target_os = "windows"))]
    mod not_windows {
        use bstr::Finder;
        use once_cell::sync::Lazy;
        finder!(pub MIDDLEWARE_FINDER = "/kolo/middleware.py");
        finder!(pub DJANGO_SETUP_FINDER = "django/__init__.py");
        finder!(pub TEMPLATE_FINDER = "django/template/backends/django.py");
        finder!(pub HUEY_FINDER = "/huey/api.py");
        finder!(pub REQUESTS_FINDER = "requests/sessions");
        finder!(pub HTTPX_FINDER = "httpx/_client.py");
        finder!(pub URLLIB_FINDER = "urllib/request");
        finder!(pub URLLIB3_FINDER = "urllib3/connectionpool");
        finder!(pub LOGGING_FINDER = "/logging/");
        finder!(pub SQL_FINDER = "/django/db/models/sql/compiler.py");
        finder!(pub PYTEST_FINDER = "kolo/pytest_plugin.py");
        finder!(pub UNITTEST_FINDER = "unittest/result.py");
        finder!(pub LIBRARY_FINDERS = "lib/python", "/site-packages/");
        finder!(pub KOLO_FINDERS = "/kolo/middleware", "/kolo/profiler", "/kolo/serialize", "/kolo/pytest_plugin.py");
    }
    #[cfg(not(target_os = "windows"))]
    use not_windows::*;

    fn timestamp() -> f64 {
        SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .expect("System time is before unix epoch")
            .as_secs_f64()
    }

    fn frame_path(frame: &PyFrame, py: Python) -> Result<String, PyErr> {
        let f_code = frame.getattr(intern!(py, "f_code"))?;
        let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
        let filename = co_filename.extract::<String>()?;
        let lineno = frame.getattr(intern!(py, "f_lineno"))?;
        let path = match Path::new(&filename).canonicalize() {
            Ok(path) => path,
            Err(_) => return Ok(format!("{}:{}", filename, lineno)),
        };
        let dir = current_dir()
            .expect("Current directory is invalid")
            .canonicalize()?;
        let relative_path = match path.strip_prefix(&dir) {
            Ok(relative_path) => relative_path,
            Err(_) => &path,
        };
        Ok(format!("{}:{}", relative_path.display(), lineno))
    }

    fn get_qualname(frame: &PyFrame, py: Python) -> Result<Option<String>, PyErr> {
        let f_code = frame.getattr(intern!(py, "f_code"))?;
        match f_code.getattr(intern!(py, "co_qualname")) {
            Ok(qualname) => {
                let globals = frame.getattr(intern!(py, "f_globals"))?;
                let module = globals.get_item("__name__")?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyAttributeError>(py) => {}
            Err(err) => return Err(err),
        }

        let co_name = f_code.getattr(intern!(py, "co_name"))?;
        let name = co_name.extract::<String>()?;
        if name.as_str() == "<module>" {
            let globals = frame.getattr(intern!(py, "f_globals"))?;
            let module = globals.get_item("__name__")?;
            return Ok(Some(format!("{}.<module>", module)));
        }

        match _get_qualname_inner(frame, py, co_name) {
            Ok(qualname) => Ok(qualname),
            Err(_) => Ok(None),
        }
    }

    fn _get_qualname_inner(
        frame: &PyFrame,
        py: Python,
        co_name: &PyAny,
    ) -> Result<Option<String>, PyErr> {
        let outer_frame = frame.getattr(intern!(py, "f_back"))?;
        if outer_frame.is_none() {
            return Ok(None);
        }

        let outer_frame_locals = outer_frame.getattr(intern!(py, "f_locals"))?;
        match outer_frame_locals.get_item(co_name) {
            Ok(function) => {
                let module = function.getattr(intern!(py, "__module__"))?;
                let qualname = function.getattr(intern!(py, "__qualname__"))?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        }

        let locals = frame.getattr(intern!(py, "f_locals"))?;
        let inspect = PyModule::import(py, "inspect")?;
        let getattr_static = inspect.getattr(intern!(py, "getattr_static"))?;
        match locals.get_item("self") {
            Ok(locals_self) => {
                let function = getattr_static.call1((locals_self, co_name))?;
                let builtins = py.import("builtins")?;
                let property = builtins.getattr(intern!(py, "property"))?;
                let property = property.extract()?;
                let function = match function.is_instance(property)? {
                    true => function.getattr(intern!(py, "fget"))?,
                    false => function,
                };
                let module = function.getattr(intern!(py, "__module__"))?;
                let qualname = function.getattr(intern!(py, "__qualname__"))?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        };

        match locals.get_item("cls") {
            Ok(cls) if cls.is_instance_of::<PyType>()? => {
                let function = getattr_static.call1((cls, co_name))?;
                let module = function.getattr(intern!(py, "__module__"))?;
                let qualname = function.getattr(intern!(py, "__qualname__"))?;
                return Ok(Some(format!("{}.{}", module, qualname)));
            }
            Ok(_) => {}
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
            Err(_) => return Ok(None),
        }
        let globals = frame.getattr(intern!(py, "f_globals"))?;
        match locals.get_item("__qualname__") {
            Ok(qualname) => {
                let module = globals.get_item("__name__")?;
                Ok(Some(format!("{}.{}", module, qualname)))
            }
            Err(err) if err.is_instance_of::<PyKeyError>(py) => {
                let function = globals.get_item(co_name)?;
                let module = function.getattr(intern!(py, "__module__"))?;
                let qualname = function.getattr(intern!(py, "__qualname__"))?;
                Ok(Some(format!("{}.{}", module, qualname)))
            }
            Err(_) => Ok(None),
        }
    }

    fn dump_json(py: Python, data: &PyAny) -> Result<serde_json::Value, PyErr> {
        let serialize = PyModule::import(py, "kolo.serialize")?;
        let args = PyTuple::new(py, [&data]);
        let json_data = serialize.call_method1("dump_json", args)?;
        let json_data = json_data.extract::<String>()?;
        let json_data = match serde_json::from_str(&json_data) {
            Ok(value) => value,
            Err(err) => {
                eprintln!("Could not load json: {}", json_data);
                let message = format!("{} {}", err, json_data);
                let pyerr = PyErr::new::<PyValueError, _>(message);
                return Err(pyerr);
            }
        };
        Ok(json_data)
    }

    fn current_thread(py: Python) -> Result<(&str, usize), PyErr> {
        let threading = PyModule::import(py, "threading")?;
        let thread = threading.call_method0("current_thread")?;
        let thread_name = thread.getattr(intern!(py, "name"))?;
        let thread_name = thread_name.extract()?;
        let native_id = thread.getattr(intern!(py, "native_id"))?;
        let native_id = native_id.extract()?;
        Ok((thread_name, native_id))
    }

    fn use_django_filter(filename: &str) -> bool {
        MIDDLEWARE_FINDER.find(filename).is_some()
    }

    fn use_django_setup_filter(filename: &str) -> bool {
        DJANGO_SETUP_FINDER.find(filename).is_some()
    }

    fn use_django_template_filter(filename: &str) -> bool {
        TEMPLATE_FINDER.find(filename).is_some()
    }

    fn use_celery_filter(filename: &str) -> bool {
        CELERY_FINDER.find(filename).is_some() && SENTRY_FINDER.find(filename).is_none()
    }

    fn use_huey_filter(
        filename: &str,
        huey_filter: &PyAny,
        py: Python,
        pyframe: &PyFrame,
    ) -> Result<bool, PyErr> {
        if HUEY_FINDER.find(filename).is_some() {
            let task_class = huey_filter.getattr(intern!(py, "klass"))?;
            if task_class.is_none() {
                let huey_api = PyModule::import(py, "huey.api")?;
                let task_class = huey_api.getattr(intern!(py, "Task"))?;
                huey_filter.setattr("klass", task_class)?;
            }

            let task_class = huey_filter.getattr(intern!(py, "klass"))?;
            let task_class = task_class.downcast()?;
            let frame_locals = pyframe.getattr(intern!(py, "f_locals"))?;
            let task = frame_locals.get_item("self")?;
            task.is_instance(task_class)
        } else {
            Ok(false)
        }
    }

    fn use_httpx_filter(filename: &str) -> bool {
        HTTPX_FINDER.find(filename).is_some()
    }

    fn use_requests_filter(filename: &str) -> bool {
        REQUESTS_FINDER.find(filename).is_some()
    }

    fn use_urllib_filter(filename: &str) -> bool {
        URLLIB_FINDER.find(filename).is_some()
    }

    fn use_urllib3_filter(filename: &str) -> bool {
        URLLIB3_FINDER.find(filename).is_some()
    }

    fn use_exception_filter(filename: &str, event: &str) -> bool {
        event == "call" && DJANGO_FINDER.find(filename).is_some()
    }

    fn use_logging_filter(filename: &str, event: &str) -> bool {
        event == "return" && LOGGING_FINDER.find(filename).is_some()
    }

    fn use_sql_filter(
        filename: &str,
        sql_filter: &PyAny,
        py: Python,
        pyframe: &PyFrame,
    ) -> Result<bool, PyErr> {
        if SQL_FINDER.find(filename).is_some() {
            let sql_filter_class = sql_filter.get_type();
            if sql_filter_class.getattr(intern!(py, "klass"))?.is_none() {
                let compiler = PyModule::import(py, "django.db.models.sql.compiler")?;
                let sql_update_compiler = compiler.getattr(intern!(py, "SQLUpdateCompiler"))?;
                sql_filter_class.setattr("klass", sql_update_compiler)?;
            }
            let f_code = pyframe.getattr(intern!(py, "f_code"))?;
            Ok(!f_code.is(sql_filter_class
                .getattr(intern!(py, "klass"))?
                .getattr(intern!(py, "execute_sql"))?
                .getattr(intern!(py, "__code__"))?))
        } else {
            Ok(false)
        }
    }

    fn use_pytest_filter(filename: &str, event: &str) -> bool {
        event == "call" && PYTEST_FINDER.find(filename).is_some()
    }

    fn use_unittest_filter(filename: &str, event: &str) -> bool {
        event == "call" && UNITTEST_FINDER.find(filename).is_some()
    }

    fn process_default_include_frames(
        py: Python,
        obj: &KoloProfiler,
        frame: &PyObject,
        pyframe: &PyFrame,
        event: &str,
        arg: &PyObject,
        name: &str,
        filename: &str,
    ) -> Result<bool, PyErr> {
        let filter = match name {
            "get_response" => {
                if use_django_filter(filename) {
                    obj.default_include_frames[0].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "render" => {
                if use_django_template_filter(filename) {
                    obj.default_include_frames[1].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "apply_async" => {
                if use_celery_filter(filename) {
                    obj.default_include_frames[2].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "execute" => {
                let huey_filter = obj.default_include_frames[3].as_ref(py);
                if use_huey_filter(filename, huey_filter, py, pyframe)? {
                    huey_filter
                } else {
                    return Ok(false);
                }
            }
            "send" => {
                if use_requests_filter(filename) {
                    obj.default_include_frames[4].as_ref(py)
                } else if use_httpx_filter(filename) {
                    obj.default_include_frames[12].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "do_open" => {
                if use_urllib_filter(filename) {
                    obj.default_include_frames[5].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "urlopen" => {
                if use_urllib3_filter(filename) {
                    obj.default_include_frames[6].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "handle_uncaught_exception" => {
                if use_exception_filter(filename, event) {
                    obj.default_include_frames[7].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "_log" => {
                if use_logging_filter(filename, event) {
                    obj.default_include_frames[8].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "execute_sql" => {
                let sql_filter = obj.default_include_frames[9].as_ref(py);
                if use_sql_filter(filename, sql_filter, py, pyframe)? {
                    sql_filter
                } else {
                    return Ok(false);
                }
            }
            "startTest" => {
                if use_unittest_filter(filename, event) {
                    obj.default_include_frames[10].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "stopTest" => {
                if use_unittest_filter(filename, event) {
                    obj.default_include_frames[10].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "pytest_runtest_logstart" => {
                if use_pytest_filter(filename, event) {
                    obj.default_include_frames[11].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "pytest_runtest_logfinish" => {
                if use_pytest_filter(filename, event) {
                    obj.default_include_frames[11].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            "setup" => {
                if use_django_setup_filter(filename) {
                    obj.default_include_frames[13].as_ref(py)
                } else {
                    return Ok(false);
                }
            }
            _ => return Ok(false),
        };

        let py_event = event.to_object(py);
        let call_frames = obj.call_frames.get_or_default().borrow().clone();
        let call_frames = PyList::new(py, call_frames);
        let args = PyTuple::new(py, [frame, &py_event, arg, &call_frames.into()]);
        let data = filter.call_method1("process", args)?;
        if data.is_none() {
            return Ok(true);
        }

        let json_data = dump_json(py, data)?;

        let frame_type = json_data["type"].clone();
        if obj.one_trace_per_test && frame_type == "start_test" {
            let trace_id = Ulid::new();
            let trace_id = format!("trc_{}", trace_id.to_string());
            let mut self_trace_id = obj.trace_id.lock().unwrap();
            *self_trace_id = trace_id;

            obj.start_test_index.store(
                obj.frames_of_interest.lock().unwrap().len(),
                Ordering::Release,
            );
            let mut start_test_indices = obj.start_test_indices.lock().unwrap();
            *start_test_indices = obj
                .frames
                .lock()
                .unwrap()
                .iter()
                .map(|(thread_id, frames)| (*thread_id, frames.len()))
                .collect::<HashMap<usize, usize>>();
        }

        obj.push_frame_data(py, json_data)?;

        if obj.one_trace_per_test && frame_type == "end_test" {
            obj.save_in_db(py)?;
        }
        Ok(true)
    }

    fn library_filter(co_filename: &str) -> bool {
        for finder in LIBRARY_FINDERS.iter() {
            if finder.find(co_filename).is_some() {
                return true;
            }
        }
        #[cfg(target_os = "windows")]
        {
            (LOWER_PYTHON_FINDER.find(co_filename).is_some()
                || UPPER_PYTHON_FINDER.find(co_filename).is_some())
                && (LOWER_LIB_FINDER.find(co_filename).is_some()
                    || UPPER_LIB_FINDER.find(co_filename).is_some())
        }
        #[cfg(not(target_os = "windows"))]
        false
    }

    fn frozen_filter(co_filename: &str) -> bool {
        FROZEN_FINDER.find(co_filename).is_some()
    }

    fn exec_filter(co_filename: &str) -> bool {
        EXEC_FINDER.find(co_filename).is_some()
    }

    fn kolo_filter(co_filename: &str) -> bool {
        KOLO_FINDERS
            .iter()
            .any(|finder| finder.find(co_filename).is_some())
    }

    fn module_init_filter(co_name: &str) -> bool {
        co_name == "<module>"
    }

    fn attrs_filter(co_filename: &str, pyframe: &PyFrame, py: Python) -> Result<bool, PyErr> {
        if co_filename.starts_with("<attrs generated") {
            return Ok(true);
        }

        let previous = pyframe.getattr(intern!(py, "f_back"))?;
        if previous.is_none() {
            return Ok(false);
        }

        let f_code = previous.getattr(intern!(py, "f_code"))?;
        let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
        let co_filename = co_filename.extract::<String>()?;

        #[cfg(target_os = "windows")]
        let make_path = "attr\\_make.py";
        #[cfg(not(target_os = "windows"))]
        let make_path = "attr/_make.py";

        if co_filename.is_empty() {
            let previous = previous.getattr(intern!(py, "f_back"))?;
            if previous.is_none() {
                return Ok(false);
            }
            let f_code = previous.getattr(intern!(py, "f_code"))?;
            let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
            let co_filename = co_filename.extract::<String>()?;
            Ok(co_filename.ends_with(make_path))
        } else {
            Ok(co_filename.ends_with(make_path))
        }
    }

    fn process_default_ignore_frames(
        pyframe: &PyFrame,
        co_name: &str,
        co_filename: &str,
        py: Python,
    ) -> Result<bool, PyErr> {
        if library_filter(co_filename) {
            return Ok(true);
        }

        if frozen_filter(co_filename) {
            return Ok(true);
        }

        if kolo_filter(co_filename) {
            return Ok(true);
        }

        if module_init_filter(co_name) {
            return Ok(true);
        }

        if exec_filter(co_filename) {
            return Ok(true);
        }

        // We don't need a match block here because the
        // return value is already in the right format
        attrs_filter(co_filename, pyframe, py)
    }

    // Safety:
    //
    // We match the type signature of `Py_tracefunc`.
    //
    // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/type.Py_tracefunc.html
    extern "C" fn profile_callback(
        _obj: *mut ffi::PyObject,
        _frame: *mut ffi::PyFrameObject,
        what: c_int,
        _arg: *mut ffi::PyObject,
    ) -> c_int {
        let event = match what {
            ffi::PyTrace_CALL => "call",
            ffi::PyTrace_RETURN => "return",
            _ => return 0,
        };
        let _frame = _frame as *mut ffi::PyObject;
        Python::with_gil(|py| {
            // Safety:
            //
            // `from_borrowed_ptr_or_err` must be called in an unsafe block.
            //
            // `_obj` is a reference to our `KoloProfiler` wrapped up in a Python object, so
            // we can safely convert it from an `ffi::PyObject` to a `PyObject`.
            //
            // We borrow the object so we don't break reference counting.
            //
            // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
            // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
            let obj = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _obj) } {
                Ok(obj) => obj,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };
            let profiler = match obj.extract::<PyRef<KoloProfiler>>(py) {
                Ok(profiler) => profiler,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };

            // Safety:
            //
            // `from_borrowed_ptr_or_err` must be called in an unsafe block.
            //
            // `_frame` is an `ffi::PyFrameObject` which can be converted safely
            // to a `PyObject`. We can later convert it into a `pyo3::types::PyFrame`.
            //
            // We borrow the object so we don't break reference counting.
            //
            // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
            // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
            let frame = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _frame) } {
                Ok(frame) => frame,
                Err(err) => {
                    err.restore(py);
                    return -1;
                }
            };

            // Safety:
            //
            // `from_borrowed_ptr_or_opt` must be called in an unsafe block.
            //
            // `_arg` is either a `Py_None` (PyTrace_CALL) or any PyObject (PyTrace_RETURN) or
            // NULL (PyTrace_RETURN). The first two can be unwrapped as a PyObject. `NULL` we
            // convert to a `py.None()`.
            //
            // We borrow the object so we don't break reference counting.
            //
            // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_opt
            // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
            let arg = match unsafe { PyObject::from_borrowed_ptr_or_opt(py, _arg) } {
                Some(arg) => arg,
                // TODO: Perhaps better exception handling here?
                None => py.None(),
            };

            match profiler.profile(frame, arg, event, py) {
                Ok(_) => 0,
                Err(err) => {
                    let logging = PyModule::import(py, "logging").unwrap();
                    let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();
                    let kwargs = PyDict::new(py);
                    kwargs.set_item("exc_info", err).unwrap();
                    logger
                        .call_method("warning", ("Unexpected exception in Rust:",), Some(kwargs))
                        .unwrap();
                    0
                }
            }
        })
    }

    #[pyclass(module = "kolo._kolo", frozen)]
    struct KoloProfiler {
        db_path: String,
        one_trace_per_test: bool,
        trace_id: Mutex<String>,
        frames_of_interest: Mutex<Vec<serde_json::Value>>,
        frames: Mutex<HashMap<usize, Vec<serde_json::Value>>>,
        config: PyObject,
        include_frames: Vec<Finder<'static>>,
        ignore_frames: Vec<Finder<'static>>,
        default_include_frames: Vec<PyObject>,
        call_frames: ThreadLocal<RefCell<Vec<(PyObject, String)>>>,
        timestamp: f64,
        _frame_ids: ThreadLocal<RefCell<HashMap<usize, String>>>,
        start_test_index: AtomicUsize,
        start_test_indices: Mutex<HashMap<usize, usize>>,
        main_thread_id: usize,
        source: String,
    }

    #[pymethods]
    impl KoloProfiler {
        fn save_request_in_db(&self) -> Result<(), PyErr> {
            Python::with_gil(|py| self.save_in_db(py))
        }

        fn register_threading_profiler(
            slf: PyRef<'_, Self>,
            _frame: PyObject,
            _event: PyObject,
            _arg: PyObject,
        ) -> Result<(), PyErr> {
            // Safety:
            //
            // PyEval_SetProfile takes two arguments:
            //  * trace_func: Option<Py_tracefunc>
            //  * arg1:       *mut PyObject
            //
            // `profile_callback` matches the signature of a `Py_tracefunc`, so we only
            // need to wrap it in `Some`.
            // `slf.into_ptr()` is a pointer to our Rust profiler instance as a Python
            // object.
            //
            // We must also hold the GIL, which we do because we're called from python.
            //
            // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
            // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
            unsafe {
                ffi::PyEval_SetProfile(Some(profile_callback), slf.into_ptr());
            }
            Ok(())
        }
    }

    impl KoloProfiler {
        fn save_in_db(&self, py: Python) -> Result<(), PyErr> {
            let version = PyModule::import(py, "kolo.version")?
                .getattr(intern!(py, "__version__"))?
                .extract::<String>()?;
            let commit_sha = PyModule::import(py, "kolo.git")?
                .getattr(intern!(py, "COMMIT_SHA"))?
                .extract::<Option<String>>()?;
            let argv = PyModule::import(py, "sys")?
                .getattr(intern!(py, "argv"))?
                .extract::<Vec<String>>()?;
            let frames_of_interest = &self.frames_of_interest.lock().unwrap()
                [self.start_test_index.load(Ordering::Acquire)..];
            let frames = self.frames.lock().unwrap();
            let thread_frames: HashMap<_, _> = frames
                .iter()
                .map(|(thread_id, frames)| {
                    (
                        thread_id,
                        &frames[*self
                            .start_test_indices
                            .lock()
                            .unwrap()
                            .get(thread_id)
                            .unwrap_or(&0)..],
                    )
                })
                .collect();
            let data = json!({
                "command_line_args": argv,
                "current_commit_sha": commit_sha,
                "frames": thread_frames,
                "frames_of_interest": frames_of_interest,
                "main_thread_id": format!("{}", self.main_thread_id),
                "meta": {"version": version, "source": self.source, "use_frame_boundaries": true},
                "timestamp": self.timestamp,
                "trace_id": self.trace_id,
            });
            let config = self.config.as_ref(py);
            let wal_mode = match config.get_item("wal_mode") {
                Ok(wal_mode) => Some(wal_mode),
                Err(_) => None,
            };
            let db = PyModule::import(py, "kolo.db")?;
            let save = db.getattr(intern!(py, "save_invocation_in_sqlite"))?;
            let trace_id = self.trace_id.lock().unwrap().clone();
            save.call1((&self.db_path, &trace_id, data.to_string(), wal_mode))?;
            Ok(())
        }

        fn process_frame(
            &self,
            frame: PyObject,
            event: &str,
            arg: PyObject,
            py: Python,
        ) -> Result<(), PyErr> {
            let (thread_name, native_id) = current_thread(py)?;
            let user_code_call_site = match event {
                "call" => match self.call_frames.get_or_default().borrow().last() {
                    Some((call_frame, call_frame_id)) => {
                        let pyframe = call_frame.downcast::<PyFrame>(py)?;
                        Some(json!({
                            "call_frame_id": call_frame_id,
                            "line_number": pyframe.getattr(intern!(py, "f_lineno"))?.extract::<i32>()?,
                        }))
                    }
                    None => None,
                },
                _ => None,
            };
            let pyframe = frame.downcast::<PyFrame>(py)?;
            let arg = arg.downcast::<PyAny>(py)?;
            let f_code = pyframe.getattr(intern!(py, "f_code"))?;
            let co_name = f_code.getattr(intern!(py, "co_name"))?;
            let name = co_name.extract::<String>()?;
            let pyframe_id = pyframe.as_ptr() as usize;
            let path = frame_path(pyframe, py)?;
            let qualname = get_qualname(pyframe, py)?;
            let locals = pyframe.getattr(intern!(py, "f_locals"))?;
            let json_locals = dump_json(py, locals)?;

            match event {
                "call" => {
                    let frame_ulid = Ulid::new();
                    let frame_id = format!("frm_{}", frame_ulid.to_string());
                    self._frame_ids
                        .get_or_default()
                        .borrow_mut()
                        .insert(pyframe_id, frame_id);
                    let frame_id = format!("frm_{}", frame_ulid.to_string());
                    self.call_frames
                        .get_or_default()
                        .borrow_mut()
                        .push((frame, frame_id));
                }
                "return" => {
                    if let Some(e) = self.call_frames.get() {
                        e.borrow_mut().pop();
                    }
                }
                _ => {}
            }

            let frame_data = json!({
                "path": path,
                "co_name": name,
                "qualname": qualname,
                "event": event,
                "frame_id": self._frame_ids.get_or_default().borrow().get(&pyframe_id).cloned(),
                "arg": dump_json(py, arg)?,
                "locals": json_locals,
                "thread": thread_name,
                "thread_native_id": native_id,
                "timestamp": timestamp(),
                "type": "frame",
                "user_code_call_site": user_code_call_site,
            });

            self.push_frame_data(py, frame_data)
        }

        fn push_frame_data(&self, py: Python, json_data: serde_json::Value) -> Result<(), PyErr> {
            let use_threading = match self.config.as_ref(py).get_item("threading") {
                Ok(threading) => threading.extract::<bool>().unwrap_or(false),
                Err(_) => false,
            };
            let (_, native_id) = current_thread(py)?;
            if !use_threading || native_id == self.main_thread_id {
                self.frames_of_interest.lock().unwrap().push(json_data);
            } else {
                self.frames
                    .lock()
                    .unwrap()
                    .entry(native_id)
                    .or_default()
                    .push(json_data);
            };
            Ok(())
        }

        fn process_include_frames(&self, filename: &str) -> bool {
            self.include_frames
                .iter()
                .any(|finder| finder.find(filename).is_some())
        }

        fn process_ignore_frames(&self, filename: &str) -> bool {
            self.ignore_frames
                .iter()
                .any(|finder| finder.find(filename).is_some())
        }

        fn profile(
            &self,
            frame: PyObject,
            arg: PyObject,
            event: &str,
            py: Python,
        ) -> Result<(), PyErr> {
            let pyframe = frame.as_ref(py);
            let pyframe = pyframe.downcast::<PyFrame>()?;
            let f_code = pyframe.getattr(intern!(py, "f_code"))?;
            let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
            let filename = co_filename.extract::<String>()?;

            if self.process_include_frames(&filename) {
                self.process_frame(frame, event, arg, py)?;
                return Ok(());
            };

            if self.process_ignore_frames(&filename) {
                return Ok(());
            }

            let co_name = f_code.getattr(intern!(py, "co_name"))?;
            let name = co_name.extract::<String>()?;

            if process_default_include_frames(
                py, self, &frame, pyframe, event, &arg, &name, &filename,
            )? {
                return Ok(());
            }

            if process_default_ignore_frames(pyframe, &name, &filename, py)? {
                return Ok(());
            }

            self.process_frame(frame, event, arg, py)
        }
    }

    #[pyfunction]
    fn register_profiler(profiler: PyObject) -> Result<(), PyErr> {
        Python::with_gil(|py| {
            let py_profiler = profiler.as_ref(py);
            if !py_profiler.is_callable() {
                return Err(PyTypeError::new_err("profiler object is not callable"));
            }

            let config = py_profiler.getattr(intern!(py, "config"))?;
            let filters = config.get_item("filters");
            let include_frames = match filters {
                Ok(filters) => match filters.get_item("include_frames") {
                    Ok(include_frames) => include_frames
                        .extract::<Vec<&str>>()?
                        .iter()
                        .map(Finder::new)
                        .map(|finder| finder.into_owned())
                        .collect(),
                    Err(_) => Vec::new(),
                },
                Err(_) => Vec::new(),
            };
            let ignore_frames = match filters {
                Ok(filters) => match filters.get_item("ignore_frames") {
                    Ok(ignore_frames) => ignore_frames
                        .extract::<Vec<&str>>()?
                        .iter()
                        .map(Finder::new)
                        .map(|finder| finder.into_owned())
                        .collect(),
                    Err(_) => Vec::new(),
                },
                Err(_) => Vec::new(),
            };
            let threading = PyModule::import(py, "threading")?;
            let main_thread = threading.call_method0(intern!(py, "main_thread"))?;
            let main_thread_id = main_thread.getattr(intern!(py, "native_id"))?;
            let main_thread_id = main_thread_id.extract()?;
            let rust_profiler = KoloProfiler {
                db_path: py_profiler
                    .getattr(intern!(py, "db_path"))?
                    .str()?
                    .extract()?,
                one_trace_per_test: py_profiler
                    .getattr(intern!(py, "one_trace_per_test"))?
                    .extract()?,
                trace_id: py_profiler
                    .getattr(intern!(py, "trace_id"))?
                    .extract::<String>()?
                    .into(),
                source: py_profiler
                    .getattr(intern!(py, "source"))?
                    .extract::<String>()?,
                frames: HashMap::new().into(),
                frames_of_interest: Vec::new().into(),
                config: config.into(),
                include_frames,
                ignore_frames,
                default_include_frames: py_profiler
                    .getattr(intern!(py, "_default_include_frames"))?
                    .extract()?,
                call_frames: ThreadLocal::new(),
                timestamp: timestamp(),
                _frame_ids: ThreadLocal::new(),
                start_test_index: 0.into(),
                start_test_indices: HashMap::new().into(),
                main_thread_id,
            };
            let py_rust_profiler = rust_profiler.into_py(py);
            let py_rust_profiler_2 = py_rust_profiler.clone();
            py_profiler.setattr("rust_profiler", &py_rust_profiler)?;

            // Safety:
            //
            // PyEval_SetProfile takes two arguments:
            //  * trace_func: Option<Py_tracefunc>
            //  * arg1:       *mut PyObject
            //
            // `profile_callback` matches the signature of a `Py_tracefunc`, so we only
            // need to wrap it in `Some`.
            // `py_rust_profiler.into_ptr()` is a pointer to our Rust profiler
            // instance as a Python object.
            //
            // We must also hold the GIL, which we explicitly do above.
            //
            // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
            // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
            unsafe {
                ffi::PyEval_SetProfile(Some(profile_callback), py_rust_profiler.into_ptr());
            }
            let use_threading = match config.get_item("threading") {
                Ok(threading) => threading.extract::<bool>().unwrap_or(false),
                Err(_) => false,
            };
            if use_threading {
                let args =
                    PyTuple::new(
                        py,
                        [py_rust_profiler_2
                            .getattr(py, intern!(py, "register_threading_profiler"))?],
                    );
                threading.call_method1("setprofile", args)?;
            }

            Ok(())
        })
    }

    // Safety:
    //
    // We match the type signature of `Py_tracefunc`.
    //
    // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/type.Py_tracefunc.html
    extern "C" fn noop_profile(
        _obj: *mut ffi::PyObject,
        _frame: *mut ffi::PyFrameObject,
        _what: c_int,
        _arg: *mut ffi::PyObject,
    ) -> c_int {
        0
    }

    #[pyfunction]
    fn register_noop_profiler() {
        // Safety:
        //
        // PyEval_SetProfile takes two arguments:
        //  * trace_func: Option<Py_tracefunc>
        //  * arg1:       *mut PyObject
        //
        // `noop_profile` matches the signature of a `Py_tracefunc`, so
        // we only need to wrap it in `Some`.
        // `arg1` can accept a NULL pointer, so that's what we pass.
        //
        // PyEval_SetProfile also requires we hold the GIL, so we wrap the
        // `unsafe` block in `Python::with_gil`.
        //
        // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
        // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
        Python::with_gil(|_py| unsafe {
            ffi::PyEval_SetProfile(Some(noop_profile), ptr::null_mut());
        })
    }

    #[pymodule]
    fn _kolo(_py: Python, m: &PyModule) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(register_profiler, m)?)?;
        m.add_function(wrap_pyfunction!(register_noop_profiler, m)?)?;
        Ok(())
    }
}

#[cfg(not(PyPy))]
pub use _kolo::*;
