'use strict';
angular.module('myApp')
  .controller('AlunoCtrl', function ($scope, $http, Exercise) {

    $http.get("/api/alunos/").then(function(response) {
        $scope.alunos = response.data;
        console.log($scope.alunos[0])
    });

  });
