import 'package:flavour_swipe/pages/ranking_page/ranking_page_widget.dart';
import 'package:flavour_swipe/pages/swipe_page/api_call_swipe_page.dart';
import 'package:flavour_swipe/pages/swipe_page/swipeable_card.dart';
import '../swipe_detail_page/swipe_detail_page_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_swipeable_stack.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
export 'swipe_page_model.dart';

class SwipePageWidget extends StatefulWidget {
  const SwipePageWidget({super.key});

  @override
  _SwipePageWidgetState createState() => _SwipePageWidgetState();
}

class _SwipePageWidgetState extends State<SwipePageWidget> {
  late SwipePageModel _model;
  final List<int> selectedRecipeIds = [];
  List<Recipe?>? recipes;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => SwipePageModel());
    loadRecipes(); // Rufen Sie hier Ihre asynchrone Funktion auf
  }

  void loadRecipes() async {
    try {
      List<Recipe> loadedRecipes = await getRecipeDataList();
      setState(() {
        recipes = loadedRecipes;
      });
    } catch (e) {
      print('Fehler beim Laden der Rezeptdaten: $e');
    }
  }

  @override
  void dispose() {
    _model.dispose();
    super.dispose();
  }

  void addRecipeIdAndNavigateIfNecessary(int recipeId) {
    setState(() {
      selectedRecipeIds.add(recipeId);
    });

    if (selectedRecipeIds.length == 3) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => RankingPageWidget(
            recipeIds: selectedRecipeIds,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isiOS) {
      SystemChrome.setSystemUIOverlayStyle(
        SystemUiOverlayStyle(
          statusBarBrightness: Theme.of(context).brightness,
          systemStatusBarContrastEnforced: true,
        ),
      );
    }

    return GestureDetector(
      onTap: () => _model.unfocusNode.canRequestFocus
          ? FocusScope.of(context).requestFocus(_model.unfocusNode)
          : FocusScope.of(context).unfocus(),
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: const Color(0xFF57636C),
        appBar: AppBar(
          backgroundColor: const Color(0xFF57636C),
          automaticallyImplyLeading: false,
          leading: FlutterFlowIconButton(
            borderColor: Colors.transparent,
            borderRadius: 30.0,
            borderWidth: 1.0,
            buttonSize: 60.0,
            icon: const Icon(
              Icons.arrow_back_rounded,
              color: Colors.white,
              size: 30.0,
            ),
            onPressed: () async {
              context.pop();
            },
          ),
          actions: const [],
          centerTitle: false,
          elevation: 0.0,
        ),
        body: Align(
          alignment: const AlignmentDirectional(0.00, 0.00),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Expanded(
                child: recipes == null
                    ? CircularProgressIndicator()
                    : FlutterFlowSwipeableStack(
                        topCardHeightFraction: 0.72,
                        middleCardHeightFraction: 0.68,
                        bottomCardHeightFraction: 0.75,
                        topCardWidthFraction: 0.9,
                        middleCardWidthFraction: 0.85,
                        bottomCardWidthFraction: 0.8,
                        onSwipeFn: (index) {},
                        onLeftSwipe: (index) async {
                          Recipe currentRecipe = recipes![index]!;
                          int recipeId = currentRecipe.id;
                          await submitDislike(recipeId);
                          print("submitDislike");
                        },
                        onRightSwipe: (index) async {
                          Recipe currentRecipe = recipes![index]!;
                          int recipeId = currentRecipe.id;
                          await submitLike(recipeId);
                          print("submitLike");
                          addRecipeIdAndNavigateIfNecessary(recipeId);
                        },
                        onUpSwipe: (index) async {
                          // Abrufen der aktuellen Rezept-ID
                          Recipe currentRecipe = recipes![index]!;
                          int recipeId = currentRecipe.id;
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => SwipeDetailPageWidget(
                                recipeId: recipeId.toString(),
                              ),
                            ),
                          );
                        },
                        onDownSwipe: (index) {},
                        itemBuilder: (context, index) {
                          Recipe recipe = recipes![index]!;
                          return SwipeableCardItem(
                            recipeID: recipe.id,
                            cookingTime: recipe.cookingTime,
                            difficulty: recipe.difficulty,
                            textTitle: recipe.title,
                            imageUrl: recipe.imageUrl,
                          );
                        },
                        itemCount: recipes!.length,
                        controller: _model.swipeableStackController,
                        enableSwipeUp: true,
                        enableSwipeDown: false,
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
