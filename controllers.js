function RobotPageInterface($scope) {
	$scope.title = "Salvius";

	$scope.alert = "Danger! Something with the robot needs your attention!";
	
	$scope.sensors = {
    sensortype: 'Sensor',
	valuetype: 'Value',
    components: [
		{"type": "Temperature",
		"reading": "71.0",
		"unit": "C"},
		{"type": "Light",
		"reading": "2.2",
		"unit": "U"},
		{"type": "Ultrasonic",
		"reading": "20.4",
		"unit": "cm"}
    ]
  };
  
  var myApp = angular.module('myApp', ['ngResource'])

	myApp.config(
		['$routeProvider', function($routeProvider) {
			$routeProvider.when('/', {
				title: 'Home',
				templateUrl: '/index.html',
				controller: 'RobotPageInterface'
			});
			$routeProvider.when('/Product/:id', {
				title: 'Product',
				templateUrl: '/Assets/Views/Product.html',
				controller: 'RobotPageInterface'
			});
		}]);

	myApp.run(['$location', '$rootScope', function($location, $rootScope) {
		$rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
			$rootScope.title = current.$route.title;
		});
	}]);
  
}