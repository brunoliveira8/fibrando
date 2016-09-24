'use strict';
angular.module('myApp').factory('Task', function($resource) {
  return $resource('/api/tasks/:taskId/', {taskId:'@id'},
  {
  	'update': { method: 'PUT' }
  });
});