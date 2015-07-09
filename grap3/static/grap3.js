angular.module('grap3App', [])

  .factory('APIService', function( $http ) {
    return {
      getGroceries: function() {
        return $http.get('/api/groceries/').then(function(result) {
          return result.data;
        });
      },
      getRecommendations: function(query) {
        return $http.get('/api/recommendation/?g=' + query).then(function(result) {
          return result.data;
        });
      },
    }
  })

  .controller('Grap3Controller', function($scope, APIService) {
    var grap3 = this;
    grap3.searchTerms = []

    grap3.addGrocery = function(grocery) {
      grap3.searchTerms.push(grocery);
      grap3.getRecommendations();
    };

    grap3.removeGrocery = function(grocery) {
      grap3.searchTerms.splice(grap3.searchTerms.indexOf(grocery), 1);
      grap3.getRecommendations();
    };

    grap3.removeAllGrocery = function() {
      grap3.searchTerms = [];
      grap3.recommendations = '';
    };

    grap3.getRecommendations = function() {
      APIService.getRecommendations(grap3.searchTerms.join(",")).then(function(data) {
        grap3.recommendations = data;
      });
    };

    grap3.getGroceries = function() {
      APIService.getGroceries().then(function(data) {
        grap3.groceryItems = data['groceries'];
      });
    };

    grap3.getGroceries();

  });