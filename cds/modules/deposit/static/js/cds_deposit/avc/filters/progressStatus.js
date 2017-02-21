function progressStatus() {
  var checkStatus = function(task, status) {
    return function(child) {
      return child.metadata._deposit.state[task] == status;
    };
  };
  return function(children) {
    var res = new Map();
    if (!children) {
      return;
    }
    ['file_download', 'file_video_metadata_extraction',
      'file_video_extract_frames', 'file_transcode'].forEach(function(task) {
      if (children.every(checkStatus(task, 'SUCCESS'))) {
        res[task] = 'SUCCESS';
      } else if (children.some(checkStatus(task, 'FAILURE'))) {
        res[task] = 'FAILURE';
      } else if (children.some(checkStatus(task, 'STARTED')) ||
        children.some(checkStatus(task, 'SUCCESS'))) {
        res[task] = 'STARTED';
      } else if (!children.every(checkStatus(task, undefined))) {
        res[task] = 'PENDING';
      }
    });
    return res;
  };
}

angular.module("cdsDeposit.filters")
  .filter('progressStatus', progressStatus);
