use mcai_worker_sdk::prelude::*;
use pyo3::prelude::*;
use std::sync::{Arc, Mutex};

/// Enum representing the job status.
///
/// This enum is essentially to be used as :func:`~mcai_worker_sdk.McaiChannel.set_job_status` argument.
#[pyclass(name = "JobStatus")]
#[derive(Clone)]
pub enum PythonJobStatus {
  Completed,
  Stopped,
  Error,
}
/// Channel object that allows sending information (status, progression) about the job to the backend.
#[pyclass(name = "McaiChannel")]
pub struct CallbackHandle {
  pub channel: Option<McaiChannel>,
  pub job_id: u64,
  pub job_status: Arc<Mutex<Option<JobStatus>>>,
}

#[pymethods]
impl CallbackHandle {
  /// Method for publishing the progression of the job.
  ///
  /// Arguments:
  ///   progression (int): progression of the job in percent.
  ///
  /// Returns:
  ///   bool: True if the publication of the progression was successfull, else False.
  #[pyo3(text_signature = "($self, progression)")]
  fn publish_job_progression(&self, value: u8) -> bool {
    publish_job_progression(self.channel.clone(), self.job_id, value).is_ok()
  }

  /// Method for checking wether the current job is stopped.
  ///
  /// Returns:
  ///   bool: True if the current job is stopped, else False.
  fn is_stopped(&self) -> bool {
    if let Some(channel) = &self.channel {
      channel.lock().unwrap().is_stopped()
    } else {
      false
    }
  }

  /// Method for setting the job status to return to the backend.
  ///
  /// Arguments:
  ///   status (:class:`~mcai_worker_sdk.JobStatus`): status of the job.
  ///
  /// Returns:
  ///   bool: True if the status has been set properly, else False.
  #[pyo3(text_signature = "($self, status)")]
  fn set_job_status(&mut self, status: PythonJobStatus) -> bool {
    let mut job_status = self.job_status.lock().unwrap();
    *job_status = match status {
      PythonJobStatus::Completed => Some(JobStatus::Completed),
      PythonJobStatus::Stopped => Some(JobStatus::Stopped),
      PythonJobStatus::Error => Some(JobStatus::Error),
    };
    job_status.is_some()
  }
}
