'use strict';
angular.module('myApp').factory('Departamento', function($resource) {
  return $resource('/api/departamentos/:departamentoId/', {departamentoId:'@id'},
  {
  	'update': { method: 'PUT' }
  });
});