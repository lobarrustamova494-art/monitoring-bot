Preparing metadata (pyproject.toml): finished with status 'error'
  error: subprocess-exited-with-error
  
  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [14 lines of output]
          Updating crates.io index
      warning: failed to write cache, path: /usr/local/cargo/registry/index/index.crates.io-1949cf8c6b5b557f/.cache/ah/as/ahash, error: Read-only file system (os error 30)
       Downloading crates ...
        Downloaded autocfg v1.1.0
      error: failed to create directory `/usr/local/cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`
      
      Caused by:
        Read-only file system (os error 30)
      💥 maturin failed
        Caused by: Cargo metadata failed. Does your crate compile with `cargo build`?
        Caused by: `cargo metadata` exited with an error:
      Error running maturin: Command '['maturin', 'pep517', 'write-dist-info', '--metadata-directory', '/tmp/pip-modern-metadata-xvinj0zf', '--interpreter', '/opt/render/project/src/.venv/bin/python3.14']' returned non-zero exit status 1.
      Checking for Rust toolchain....
      Running `maturin pep517 write-dist-info --metadata-directory /tmp/pip-modern-metadata-xvinj0zf --interpreter /opt/render/project/src/.venv/bin/python3.14`
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pydantic-core
note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
==> Build failed 😞
Menu
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys