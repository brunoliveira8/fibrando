'use strict';
angular.module('myApp')
  .controller('ExerciseCtrl', function ($scope, $http, Exercise, Task, WorkoutPlan) {

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

    $scope.addExercise = function(){
        $scope.new_exercise = new Exercise();
        $scope.new_exercise.task = $scope.selectedTask;;
        $scope.new_exercise.weight = $scope.peso;
        $scope.new_exercise.repetition = $scope.repet;
        $scope.new_exercise.sets = $scope.series;
        $scope.new_exercise.division = $scope.selectedDiv;
        $scope.new_exercise.workout_plan = $scope.workout_plan;

        $scope.new_exercise.$save({username: $scope.username}, function(data){
            //$scope.dep_name = '';
            $scope.getExercises($scope.username);

            $scope.selectedTask = "";
            $scope.peso = "";
            $scope.repet = "";
        });
        
    };

    $scope.deleteExercise = function(exerciseId){

        var exercise = Exercise.get({ username: $scope.username, exerciseId: exerciseId }, function() {
            exercise.$delete({ username: $scope.username}, function(){
                $scope.getExercises($scope.username);
            });
        }); 
    };

    $scope.updateExercise = function(data, id) {
        var exercise = Exercise.get({ username: $scope.username, exerciseId:id }, function(){

            exercise.weight = data.weight;
            exercise.sets = data.sets;
            exercise.repetition = data.repetition;

            exercise.$update({ username: $scope.username}, function(){
                $scope.getExercises($scope.username);
            });
         

        }); 
        console.log(exercise);
    };

    $http.get("/api/current_user/").then(function(response) {
        $scope.username = response.data.username;
        $scope.getExercises($scope.username);
        WorkoutPlan.get({username: $scope.username}, function(workout_plan){
            $scope.workout_plan = workout_plan;
        });

    });

    $scope.divs = ['A', 'B', 'C', 'D', 'E'];

    Task.query(function(tasks){
        $scope.tasks = tasks;
    });

    $scope.myVar = true;
    $scope.toggle = function() {
        $scope.myVar = !$scope.myVar;
    };

  });
