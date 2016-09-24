'use strict';
angular.module('myApp')
  .controller('DepartamentoCtrl', function ($scope, $http, Departamento) {

    $scope.getDepartamento = function(departamentoId){
    	Departamento.get({departamentoId:departamentoId}).$promise.then(function(departamento) {
      		console.log(departamento.name)
    	});
    };

    $scope.getDepartamentos = function(){
    	Departamento.query(function(departamentos){
    		$scope.departamentos = departamentos;
    	});
	};

    $scope.addDepartamento = function(){
    	var new_departament = new Departamento();
    	new_departament.name = $scope.dep_name;
    	new_departament.$save(function(){
			$scope.dep_name = '';
	    	$scope.getDepartamentos();
    	});
    	
    };

    $scope.deleteDepartamento = function(departamentoId){

		var departamento = Departamento.get({ departamentoId: departamentoId }, function() {
			departamento.$delete(function(){
				$scope.getDepartamentos();
			});
		});	
    };

    $scope.updateDepartamento = function(){
        
    	var departamento = Departamento.get({ departamentoId:$scope.editId }, function(){
            departamento.name = $scope.editName
            departamento.$update(function(){
                $scope.getDepartamentos();
            });
        });	
    };

    $('#editModal').on('show.bs.modal', function (event) {
	  $scope.editName = '';
	  var button = $(event.relatedTarget) // Button that triggered the modal
	  var recipient = button.data('whatever') // Extract info from data-* attributes

	  var departamento = Departamento.get({ departamentoId: recipient }, function() {
			$scope.defaultName = departamento.name;
			$scope.editId = departamento.id;
		});	  
	});

	$scope.getDepartamentos();

  });