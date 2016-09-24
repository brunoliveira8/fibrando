'use strict';
angular.module('myApp').factory('BodyScreening', function($resource) {
  return $resource('/api/screenings/:username/:screeningId/', {screeningId:'@id'},
  {
  	'update': { method: 'PUT' }
  });
});