import 'dart:convert';
import 'dart:io';

import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_swipeable_stack.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'swipe_page_model.dart';
export 'swipe_page_model.dart';
import 'package:http/http.dart' as http;

String username = "admin";
String password = "123456789.";
String credentials = "${username}:${password}";
String encoded = utf8.fuse(base64).encode(credentials);

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

// Django Backend Call
Future<void> getRecipeData(String username, String password) async {
  var url = Uri.parse('http://10.0.2.2:8000/api/recipe/');
  var response = await http
      .post(url, body: {'username': "admin", 'password': "123456789."});

  if (response.statusCode == 200) {
    // Verarbeiten der Antwort
    print('Response data: ${response.body}');
  } else {
    // Fehlerbehandlung
    print('Failed to call API. Status code: ${response.statusCode}');
    print('Response body: ${response.body}');
  }
}
