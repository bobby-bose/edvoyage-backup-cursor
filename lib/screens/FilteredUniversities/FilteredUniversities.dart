import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/screens/Study_abroad-Screen/studyabroadscreen.dart';
import 'package:frontend/screens/home_screen/SearchResults/searchexplorecourses.dart';
import 'package:frontend/screens/sort_screens/sort_home.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/models/university.dart';

class FilteredUniversitiesState {
  final List<University> universities;
  final bool isLoading;
  final String? error;
  FilteredUniversitiesState({
    required this.universities,
    required this.isLoading,
    this.error,
  });
  FilteredUniversitiesState copyWith({
    List<University>? universities,
    bool? isLoading,
    String? error,
  }) {
    return FilteredUniversitiesState(
      universities: universities ?? this.universities,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class FilteredUniversitiesNotifier
    extends StateNotifier<FilteredUniversitiesState> {
  FilteredUniversitiesNotifier()
      : super(FilteredUniversitiesState(universities: [], isLoading: false));

  Future<void> fetchFilteredUniversities({
    required List ranking,
    required List cities,
    required String rating,
    required String token,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await http.post(
        Uri.parse(BaseUrl.filtereduniversities),
        headers: {'Authorization': 'Bearer $token'},
        body: {
          'ranking': jsonEncode(ranking),
          'cities': jsonEncode(cities),
          'rating': jsonEncode(rating),
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        List<University> universities = [];
        for (var u in data) {
          universities.add(University.fromJson(u));
        }
        state = state.copyWith(universities: universities, isLoading: false);
      } else if (response.statusCode == 401) {
        state = state.copyWith(
            error: 'Unauthorized. Please login again.', isLoading: false);
      } else {
        state = state.copyWith(
            error: 'Failed to load universities', isLoading: false);
      }
    } catch (e) {
      state =
          state.copyWith(error: 'Network or server error', isLoading: false);
    }
  }

  Future<void> bookmarkUniversity(int universityId, String token) async {
    try {
      final response = await http.post(
        Uri.parse(BaseUrl.bookmarkUniversity),
        headers: {'Authorization': 'Bearer $token'},
        body: {'university_id': universityId.toString()},
      );
      if (response.statusCode == 200) {
        // Optionally update local state
        fetchFilteredUniversities(
          ranking: [],
          cities: [],
          rating: '',
          token: token,
        );
      }
    } catch (e) {
      // Optionally handle error
    }
  }
}

final filteredUniversitiesProvider = StateNotifierProvider<
    FilteredUniversitiesNotifier, FilteredUniversitiesState>((ref) {
  return FilteredUniversitiesNotifier();
});

class FilteredUniversities extends ConsumerStatefulWidget {
  final List ranking;
  final List cities;
  String rating;
  FilteredUniversities(
      {super.key,
      required this.ranking,
      required this.cities,
      required this.rating});
  @override
  ConsumerState<FilteredUniversities> createState() => _ExploreCoursesState();
}

class _ExploreCoursesState extends ConsumerState<FilteredUniversities> {
  Measurements? size;
  String token = '';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(filteredUniversitiesProvider.notifier).fetchFilteredUniversities(
            ranking: widget.ranking,
            cities: widget.cities,
            rating: widget.rating,
            token: token,
          );
    });
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    final state = ref.watch(filteredUniversitiesProvider);
    return SafeArea(
      child: Scaffold(
        backgroundColor: color3,
        appBar: AppBar(
          shape: ContinuousRectangleBorder(
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(150.0),
              bottomRight:
                  Radius.circular(150.0), // Adjust the border radius as needed
            ),
          ),
          toolbarHeight: 70.0,
          primary: false,
          backgroundColor: Colors.white,
          title: SizedBox(
            height: 30,
            child: TextFormField(
              onFieldSubmitted: (query) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => SearchExploreCourses(query: query)),
                );
              },
              decoration: InputDecoration(
                fillColor: Colors.black12,
                filled: true,
                isDense: true,
                contentPadding: EdgeInsets.fromLTRB(5, 5, 5, 0),
                hintText: "Search University",
                hintStyle: TextStyle(fontFamily: 'Poppins', color: textColor),
                prefixIcon: Icon(Icons.search, color: iconcolor, size: 20),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(40.0),
                  borderSide: BorderSide(color: grey2),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(40.0),
                  borderSide: BorderSide(color: Colors.black12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(40.0),
                  borderSide: BorderSide(color: grey2),
                ),
              ),
            ),
          ),
          leading: Padding(
            padding: const EdgeInsets.only(left: 20.0),
            child: IconButton(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: Icon(
                Icons.arrow_back_ios,
                color: Cprimary,
              ),
            ),
          ),
          actions: [
            Center(
              child: Padding(
                padding: const EdgeInsets.only(right: 15.0),
                child: IconButton(
                  onPressed: () {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) => SortHome()));
                  },
                  icon: Image.asset("assets/filter.png"),
                ),
              ),
            ),
          ],
        ),
        body: state.isLoading
            ? Center(child: CircularProgressIndicator())
            : state.error != null
                ? Center(
                    child:
                        Text(state.error!, style: TextStyle(color: Colors.red)))
                : ListView.builder(
                    itemCount: state.universities.length,
                    itemBuilder: (context, index) {
                      University university = state.universities[index];
                      return Padding(
                        padding:
                            EdgeInsets.only(left: 8.0, right: 8.0, top: 8.0),
                        child: Card(
                          semanticContainer: true,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15),
                          ),
                          elevation: 1,
                          child: Padding(
                            padding: const EdgeInsets.all(10),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  children: [
                                    Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      children: [
                                        Image.network(
                                          (university.logo ?? '').isNotEmpty
                                              ? university.logo!
                                              : 'https://via.placeholder.com/60',
                                          height: 60,
                                          width: 60,
                                        ),
                                      ],
                                    ),
                                    Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          university.name,
                                          style: TextStyle(
                                              fontSize: 15,
                                              fontFamily: 'Roboto',
                                              color: Cprimary,
                                              fontWeight: FontWeight.w600),
                                        ),
                                        vGap(4),
                                        Text(
                                          "${university.location ?? ''}, ${university.country ?? ''}",
                                          style: TextStyle(
                                              fontFamily: 'Roboto',
                                              fontSize: 12,
                                              color: grey3,
                                              fontWeight: FontWeight.w600),
                                        ),
                                        vGap(15),
                                        Row(
                                          children: [
                                            Text(
                                              "ESTD : ",
                                              style: TextStyle(
                                                  fontFamily: 'Roboto',
                                                  fontSize: 12,
                                                  color: grey3,
                                                  fontWeight: FontWeight.w600),
                                            ),
                                            Text(
                                              university.establishedYear ?? '',
                                              style: TextStyle(
                                                  fontFamily: 'Roboto',
                                                  fontSize: 12,
                                                  color: grey3,
                                                  fontWeight: FontWeight.w600),
                                            ),
                                          ],
                                        ),
                                        vGap(3),
                                        Row(
                                          children: [
                                            Text(
                                              "DV Rank",
                                              style: TextStyle(
                                                  fontFamily: 'Roboto',
                                                  fontSize: 12,
                                                  color: grey3,
                                                  fontWeight: FontWeight.w600),
                                            ),
                                            SizedBox(width: 3),
                                            RatingBar.builder(
                                              initialRating:
                                                  university.rating ?? 0.0,
                                              minRating: 1,
                                              direction: Axis.horizontal,
                                              allowHalfRating: true,
                                              itemCount: 5,
                                              itemSize: 17,
                                              itemBuilder: (context, _) => Icon(
                                                Icons.star,
                                                color: Colors.amber,
                                              ),
                                              onRatingUpdate: (rating) {
                                                // Optionally handle rating update
                                              },
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    Material(
                                        type: MaterialType.transparency,
                                        child: Ink(
                                          decoration: BoxDecoration(
                                            border: Border.all(
                                                color: Colors.white,
                                                width: 2.5),
                                            color:
                                                (university.bookmark ?? false)
                                                    ? Colors.green
                                                    : Colors.grey,
                                            shape: BoxShape.circle,
                                          ),
                                          child: InkWell(
                                            borderRadius:
                                                BorderRadius.circular(1000.0),
                                            onTap: () {
                                              ref
                                                  .read(
                                                      filteredUniversitiesProvider
                                                          .notifier)
                                                  .bookmarkUniversity(
                                                      university.id, token);
                                            },
                                            child: Padding(
                                              padding: EdgeInsets.all(8.0),
                                              child: Icon(
                                                Icons.bookmark_add_outlined,
                                                size: 20.0,
                                                color: Colors.white,
                                              ),
                                            ),
                                          ),
                                        )),
                                    Container(
                                      height: size?.hp(4),
                                      width: size?.wp(25),
                                      decoration: BoxDecoration(
                                        color: secondaryColor,
                                        borderRadius: BorderRadius.circular(5),
                                      ),
                                      child: TextButton(
                                        onPressed: () {
                                          Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                                builder: (context) =>
                                                    UniversitHomeScreen(
                                                        university:
                                                            university)),
                                          );
                                        },
                                        child: const Text(
                                          'View',
                                          style: TextStyle(
                                            fontSize: 15,
                                            fontWeight: FontWeight.w600,
                                            fontFamily: 'Roboto',
                                            color: Colors.white,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
      ),
    );
  }
}
