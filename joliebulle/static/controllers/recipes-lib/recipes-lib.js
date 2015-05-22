/*jslint nomen: true */
/*global main, _, beerCalc, recipesApp*/
recipesApp.controller('RecipeslibCtrl', ['$scope', '$http', '$filter', function ($scope, $http, $filter) {
    "use strict";
    var parser, xml, string;
    
    $scope.active = false;
    

    $scope.init = function (dataJson, ingredients) {
        $scope.recipes = dataJson;
        $scope.recipes = _.chain($scope.recipes)
            .sortBy(function (o) {return o.name.toLowerCase(); })
            .sortBy(function (o) {return o.brewer.toLowerCase(); })
            .value();
        $scope.ingredients = ingredients;
        // return $scope.recipes;
    };

    $scope.deleteLib = function (recipe) {
		$scope.recipes.splice($scope.recipes.indexOf(recipe), 1);
        main.deleteLib(recipe.path);
    };

    $scope.openRecipeClicked = function (recipe) {
        main.viewRecipeLib(recipe.path);
    };

    $scope.editIngredient = function (index) {
        $scope.showIngredientEditor = true;
        $scope.currentIng = $scope.currentRecipe.fermentables[index];
        // $scope.currentIng.index = index;
    };

    $scope.closeIngredientEditor = function () {
        $scope.showIngredientEditor = false;
        // $scope.currentRecipe.fermentables[$scope.currentIng.index] = $scope.currentIng; 

    };

    $scope.recipeSelected = function (recipe) {
        $scope.active = true;
        $scope.currentRecipe = recipe;
        $scope.calcProfile(recipe);
        $scope.sortRecipe();
        $scope.activeClass = $scope.currentRecipe.path;
        main.viewRecipeLib(recipe.path);
    };

    $scope.sortByName = function () {
        $scope.recipes = _.chain($scope.recipes)
            .sortBy(function (o) {return o.brewer.toLowerCase(); })
            .sortBy(function (o) {return o.name.toLowerCase(); })
            .value();
        return $scope.recipes;
    };

    $scope.sortByBrewer = function () {
        $scope.recipes = _.chain($scope.recipes)
            .sortBy(function (o) {return o.name.toLowerCase(); })
            .sortBy(function (o) {return o.brewer.toLowerCase(); })
            .value();
        return $scope.recipes;
    };

    $scope.sortRecipe = function () {
        $scope.currentRecipe.fermentables = _.sortBy($scope.currentRecipe.fermentables, function (o) {return parseInt(o.amount, 10); }).reverse();
        $scope.currentRecipe.hops = _.sortBy($scope.currentRecipe.hops, function (o) {return parseInt(o.time, 10); }).reverse();
        $scope.currentRecipe.miscs = _.sortBy($scope.currentRecipe.miscs, function (o) {return parseInt(o.amount, 10); }).reverse();
        return $scope.currentRecipe;
    };

    $scope.calcProfile = function (recipe) {
        recipe.ebc = Math.round(beerCalc.ebc(recipe.fermentables, recipe.volume));
        recipe.og = (Math.round(beerCalc.originalGravity(recipe) * 1000) / 1000).toFixed(3);
        recipe.fg = (Math.round(beerCalc.finalGravity(recipe) * 1000) / 1000).toFixed(3);
        recipe.ibu = Math.round(beerCalc.ibus(recipe));
        recipe.bugu = Math.round(beerCalc.bugu(recipe) * 10) / 10;
        recipe.alc = Math.round(beerCalc.alc(recipe) * 10) / 10;
    };

    $scope.fermentableSelected = function (fermentable) {
        $scope.currentIng.name = fermentable.name;
    };
    
    $scope.save = function (recipe) {
        main.saveRecipe(jb2xml.exportString(recipe), recipe.path);
    
    };
}]);



