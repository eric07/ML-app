angular.module('starter.controllers', [])

.controller('DashCtrl', function($scope, Friends) {
    Friends.get().then(function(f){
        $scope.friends = f;
      });
})

.controller('FriendsCtrl', function($scope, Friends) {
  $scope.friends = Friends.all();
})

.controller('FriendDetailCtrl', function($scope, $stateParams, Friends) {
  $scope.friend = Friends.get($stateParams.friendId);
})

.controller('AccountCtrl', function($scope) {
});
