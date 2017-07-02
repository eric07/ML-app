angular.module('starter.services', [])

/**
 * A simple example service that returns some data.
 */
.factory('Friends', function($http) {
  var Friends = function(data) {
    angular.extend(this, data);
  }

  Friends.get = function(id) {
    if (typeof id != 'undefined'){
      return $http.get('http://ml-research.herokuapp.com/'+id).then(function(response){
        return new Friends(response.data);
      });
    } else {  
      return $http.get('http://ml-research.herokuapp.com/').then(function(response){
        return new Friends(response.data);
      });
    }
  }

  return Friends;
})

.factory('Timeline', function($http){
  var Timeline = function(data) {
    angular.extend(this, data);
  }

  Timeline.get = function() {  
    return $http.get('http://seriesreminder.herokuapp.com/api/timeline').then(function(response){
      console.log(response.data);
      return new Timeline(response.data);
    });
  }

  return Timeline;
});
