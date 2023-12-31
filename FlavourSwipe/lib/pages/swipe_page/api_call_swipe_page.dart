import 'dart:convert';
import 'dart:io';
export 'swipe_page_model.dart';
import 'package:http/http.dart' as http;

String username = "admin";
String password = "123456789.";
String credentials = "${username}:${password}";
String encoded = utf8.fuse(base64).encode(credentials);
// Get All recipes
Future<List<Recipe>> getRecipeDataList() async {
  var url = Uri.parse('http://10.0.2.2:8000/api/recipe/');
  var response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      HttpHeaders.authorizationHeader: 'Basic ${encoded}',
    },
  );
  if (response.statusCode == 200) {
    List<dynamic> data = json.decode(response.body);
    print(data);
    return data.map((data) => Recipe.fromJson(data)).toList();
  } else {
    throw Exception(
        'Failed to load recipe. Status code: ${response.statusCode}, Response: {response.body}');
  }
}

// Get recipe data from a recipe ID
Future<Recipe> getRecipeData(int recipeId) async {
  print("API-Funktion aufgerufen!");
  var url =
      Uri.parse('http://10.0.2.2:8000/api/recipe/${recipeId.toString()}/');
  var response = await http.get(
    url,
    headers: {
      'Content-Type': 'application/json',
      HttpHeaders.authorizationHeader: 'Basic $encoded',
    },
  );

  if (response.statusCode == 200) {
    // Wenn der Aufruf erfolgreich ist, die Antwort deserialisieren und ein Recipe-Objekt zurückgeben
    Map<String, dynamic> data = json.decode(response.body);
    return Recipe.fromJson(data);
  } else {
    // Wenn der Aufruf fehlschlägt, eine Ausnahme werfen
    throw Exception(
        'Failed to load recipe. Status code: ${response.statusCode}, Response: ${response.body}');
  }
}

// Like a Recipe
Future<List<Recipe>> getRecipesDataListIDs(List<int> recipeIds) async {
  // Erstellen Sie eine Liste von Future<Recipe> durch Aufrufen von getRecipeData für jede ID
  List<Future<Recipe>> futures =
      recipeIds.map((id) => getRecipeData(id)).toList();

  // Warten Sie auf die Fertigstellung aller Futures und sammeln Sie die Ergebnisse
  List<Recipe> recipes = await Future.wait(futures);

  return recipes;
}

Future<void> submitLike(int receiptId) async {
  var url = Uri.parse('http://10.0.2.2:8000/api/like/$receiptId/');
  var response = await http.post(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic $encoded',
    },
  );

  if (response.statusCode == 200) {
    print('Like submitted successfully.');
  } else {
    print('Failed to submit like. Status code: ${response.statusCode}');
  }
}

// Dislike a Recipe
Future<void> submitDislike(int receiptId) async {
  var url = Uri.parse('http://10.0.2.2:8000/api/dislike/$receiptId/');
  var response = await http.post(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic $encoded',
    },
  );

  if (response.statusCode == 200) {
    print('Dislike submitted successfully.');
  } else {
    print('Failed to submit dislike. Status code: ${response.statusCode}');
  }
}

//Recipe Model
class Recipe {
  final int id;
  final int cookingTime;
  final int difficulty;
  final String title;
  final String imageUrl;
  final String description;

  Recipe({
    required this.id,
    required this.cookingTime,
    required this.difficulty,
    required this.title,
    required this.imageUrl,
    required this.description,
  });

  factory Recipe.fromJson(Map<String, dynamic> json) {
    return Recipe(
      id: json['id'],
      cookingTime: json['duration'],
      difficulty: json['difficulty'],
      title: json['name'],
      description: json['description'],
      imageUrl: json['image_id'],
    );
  }
}
