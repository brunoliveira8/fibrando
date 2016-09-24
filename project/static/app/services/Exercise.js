'use strict';
angular.module('myApp').factory('Exercise', function($resource) {
  return $resource('/api/exercises/:username/:exerciseId/', {exerciseId:'@id'},
  {
  	'update': { method: 'PUT' }
  });
});