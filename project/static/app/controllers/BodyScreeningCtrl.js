'use strict';
angular.module('myApp')
  .controller('BodyScreeningCtrl', function ($scope, $http, $location, $window, BodyScreening) {

    $scope.getScreenings = function(username){
        BodyScreening.query({username: username}, function(screenings){
            $scope.screenings = screenings;
        });
    };

    $scope.addScreening = function(){
        $scope.new_exercise = new Exercise();
        $scope.new_exercise.task = $scope.selectedTask;
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

    $scope.deleteScreening = function(screeningId){

        var screening = BodyScreening.get({ username: $scope.username, screeningId: screeningId }, function() {
            screening.$delete({ username: $scope.username}, function(){
                $scope.getScreenings($scope.username);
            });
        });
    };

    $scope.updateScreening = function(data, id) {
        var sc = BodyScreening.get({ username: $scope.username, screeningId:id }, function(){


            sc.perimetria = data.perimetria;
            sc.peitoral = data.peitoral;
            sc.abdomen = data.abdomen;
            sc.braco_direito = data.braco_direito;
            sc.braco_esquerdo = data.braco_esquerdo;
            sc.cintura = data.cintura;
            sc.quadril = data.quadril;
            sc.coxa_direita = data.coxa_direita;
            sc.coxa_esquerda = data.coxa_esquerda;

            sc.$update({ username: $scope.username});
        });
    };

    $scope.novaAvaliacao = function(){
        $window.location.href = "/create_screening/"+$scope.username;
    }


    $scope.username = $location.absUrl().split('/')[4];

    if ($scope.username == "") {
        $http.get("/api/current_user/").then(function(response) {
            $scope.user = response.data;
            $scope.username = $scope.user.username;
            $scope.getScreenings($scope.username);
        });
    }
    else {
    $scope.getScreenings($scope.username);
    }
});
