'use strict';
angular.module('myApp').factory('WorkoutPlan', function($resource) {
  return $resource('/api/current_workout_plan/:username/',
  {
  	'update': { method: 'PUT' }
  });
});