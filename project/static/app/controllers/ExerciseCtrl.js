'use strict';
angular.module('myApp')
  .controller('ExerciseCtrl', function ($scope, $http, Exercise) {

    $scope.getExercises = function(username){
        Exercise.query({username: username}, function(exercises){
            $scope.exercises = exercises;
            existent_div($scope.exercises);
        });
    };

    var existent_div = function(exercises){
        var log = [];
        angular.forEach(exercises, function(value, key) {
          if (this.indexOf(value.division) == -1) this.push(value.division);
        }, log);

        $scope.div_true = log;
    }

    $http.get("/api/current_user/").then(function(response) {
        $scope.user = response.data;
        $scope.getExercises($scope.user.username);
    });

  });
