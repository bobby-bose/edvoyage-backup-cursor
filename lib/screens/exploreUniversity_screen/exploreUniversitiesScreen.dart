import 'dart:convert';
import 'dart:math';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:http/http.dart' as http;
import '../../_env/env.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../Study_abroad-Screen/studyabroadscreen.dart';
import '../home_screen/SearchResults/searchexplorecourses.dart';
import '../sort_screens/sort_home.dart';
import '../Study_abroad-Screen/studyabroadscreen.dart'; // For UniversitHomeScreen
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/models/university.dart';
import 'package:frontend/utils/constants.dart';

// Riverpod state
class UniversityListState {
  final List<University> universities;
  final bool isLoading;
  final String? error;
  final Map<int, bool> bookmarkStates;
  final Set<int> loadingBookmarks; // Track which bookmarks are being processed
  UniversityListState({
    required this.universities,
    required this.isLoading,
    this.error,
    this.bookmarkStates = const {},
    this.loadingBookmarks = const {},
  });
  UniversityListState copyWith({
    List<University>? universities,
    bool? isLoading,
    String? error,
    Map<int, bool>? bookmarkStates,
    Set<int>? loadingBookmarks,
  }) {
    return UniversityListState(
      universities: universities ?? this.universities,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      bookmarkStates: bookmarkStates ?? this.bookmarkStates,
      loadingBookmarks: loadingBookmarks ?? this.loadingBookmarks,
    );
  }
}

class UniversityListNotifier extends StateNotifier<UniversityListState> {
  UniversityListNotifier()
      : super(UniversityListState(universities: [], isLoading: false));

  Future<void> fetchUniversities(String token) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await http.get(
        Uri.parse(BaseUrl.universityList),
        headers: {'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final universities = (data['results'] as List).map((e) {
          print('University data: $e'); // Debug log
          return University.fromJson(e);
        }).toList();

        // Initialize bookmark states for all universities
        Map<int, bool> initialBookmarkStates = {};
        for (var university in universities) {
          // Initialize as not bookmarked (false) - you can fetch actual states from backend later
          initialBookmarkStates[university.id] = university.bookmark ?? false;
        }

        state = state.copyWith(
          universities: universities,
          isLoading: false,
          bookmarkStates: initialBookmarkStates,
        );
      } else if (response.statusCode == 401) {
        state = state.copyWith(
            error: 'Unauthorized. Please login again.', isLoading: false);
      } else {
        state = state.copyWith(
            error: 'Failed to load universities', isLoading: false);
      }
    } catch (e) {
      state = state.copyWith(error: 'Network error', isLoading: false);
    }
  }

  Future<void> toggleBookmark(University university) async {
    try {
      // For testing phase, use user_id = 1
      final userId = 1;

      // Show loading state immediately
      final loadingBookmarks = Set<int>.from(state.loadingBookmarks);
      loadingBookmarks.add(university.id);
      state = state.copyWith(loadingBookmarks: loadingBookmarks);

      print('🔍 DEBUG: Toggling bookmark for university: ${university.name}');

      // Always use POST to the addFavouriteUniversity endpoint - backend handles the toggle logic
      final response = await http.post(
        Uri.parse(BaseUrl.addFavouriteUniversity),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'user_id': userId,
          'university_id': university.id,
        }),
      );

      print('🔍 DEBUG: Response status: ${response.statusCode}');
      print('🔍 DEBUG: Response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        // Parse the response to determine the action
        final responseData = jsonDecode(response.body);
        final action = responseData['action'] as String?;

        // Toggle the bookmark state based on the backend response
        final currentStates = Map<int, bool>.from(state.bookmarkStates);
        currentStates[university.id] =
            action == 'added'; // true if added, false if removed

        // Clear loading state
        final loadingBookmarks = Set<int>.from(state.loadingBookmarks);
        loadingBookmarks.remove(university.id);

        state = state.copyWith(
          bookmarkStates: currentStates,
          loadingBookmarks: loadingBookmarks,
        );

        print('✅ DEBUG: Bookmark toggled for university: ${university.name}');
        print(
            '✅ DEBUG: Action: $action, New state: ${currentStates[university.id]}');
      } else {
        // Clear loading state on error
        final loadingBookmarks = Set<int>.from(state.loadingBookmarks);
        loadingBookmarks.remove(university.id);
        state = state.copyWith(loadingBookmarks: loadingBookmarks);

        print(
            '❌ DEBUG: Failed to toggle bookmark. Status: ${response.statusCode}');
        print('❌ DEBUG: Response: ${response.body}');
      }
    } catch (e) {
      // Clear loading state on error
      final loadingBookmarks = Set<int>.from(state.loadingBookmarks);
      loadingBookmarks.remove(university.id);
      state = state.copyWith(loadingBookmarks: loadingBookmarks);

      print('❌ DEBUG: Error toggling bookmark: $e');
    }
  }
}

final universityListProvider =
    StateNotifierProvider<UniversityListNotifier, UniversityListState>((ref) {
  // You must provide the JWT token from your auth provider
  final token = '';
  final notifier = UniversityListNotifier();
  notifier.fetchUniversities(token);
  return notifier;
});

class ExploreUniversitiesScreen extends StatefulWidget {
  @override
  _ExploreCoursesState createState() => _ExploreCoursesState();
  final GlobalKey<_ExploreCoursesState> ExploreCoursesKey =
      GlobalKey<_ExploreCoursesState>();

  ExploreUniversitiesScreen({super.key});
}

class _ExploreCoursesState extends State<ExploreUniversitiesScreen> {
  Measurements? size;
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    searchController.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged() {
    setState(() {}); // Triggers rebuild to update the filtered list
  }

  String _getEstablishedYear(University university) {
    // Debug: Print all establishment year related fields
    print('University: ${university.name}');
    print('  - estd: ${university.founded_year}');
    print('  - establishedYear: ${university.establishedYear}');

    // Try different fields for establishment year
    if (university.estd != null) {
      return university.estd.toString();
    }
    if (university.establishedYear != null &&
        university.establishedYear!.isNotEmpty) {
      return university.establishedYear!;
    }
    // Check if there's any other establishment year field
    return 'N/A';
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Consumer(
      builder: (context, ref, _) {
        final state = ref.watch(universityListProvider);
        final notifier = ref.read(universityListProvider.notifier);
        final searchText = searchController.text.toLowerCase();
        final universities = state.universities;
        final filtered = searchText.isEmpty
            ? universities
            : universities
                .where((u) => u.name.toLowerCase().startsWith(searchText))
                .toList();
        if (state.isLoading) {
          return Center(child: CircularProgressIndicator());
        }
        if (state.error != null) {
          return Center(
              child: Text(state.error!, style: TextStyle(color: Colors.red)));
        }
        return SafeArea(
          child: Scaffold(
            backgroundColor: color3,
            appBar: AppBar(
              shape: ContinuousRectangleBorder(
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(150.0),
                  bottomRight: Radius.circular(150.0),
                ),
              ),
              toolbarHeight: 70.0,
              primary: false,
              backgroundColor: Colors.white,
              title: SizedBox(
                height: 30,
                child: TextFormField(
                  controller: searchController,
                  decoration: InputDecoration(
                    fillColor: Colors.black12,
                    filled: true,
                    isDense: true,
                    contentPadding: EdgeInsets.fromLTRB(5, 5, 5, 0),
                    hintText: "Search University",
                    hintStyle:
                        TextStyle(fontFamily: 'Poppins', color: textColor),
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
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => SortHome()));
                      },
                      icon: Image.asset("assets/filter.png"),
                    ),
                  ),
                ),
              ],
            ),
            body: Padding(
              padding: EdgeInsets.only(
                left: 8.0,
                right: 8.0,
                top: 8.0,
              ),
              child: ListView.builder(
                itemCount: filtered.length,
                itemBuilder: (context, index) {
                  final university = filtered[index];
                  return Card(
                    semanticContainer: true,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    elevation: 1,
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: LayoutBuilder(
                        builder: (context, constraints) {
                          return Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // University Logo
                              Container(
                                width: 60,
                                height: 60,
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: grey2, width: 1),
                                ),
                                child: ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: university.logoUrl != null &&
                                          university.logoUrl!.isNotEmpty
                                      ? Image.network(
                                          university.logoUrl!,
                                          fit: BoxFit.cover,
                                          errorBuilder:
                                              (context, error, stackTrace) {
                                            return Container(
                                              color: thirdColor,
                                              child: Image.network(
                                                'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
                                                fit: BoxFit.cover,
                                                errorBuilder: (context, error,
                                                    stackTrace) {
                                                  return Container(
                                                    color: thirdColor,
                                                    child: Icon(
                                                      Icons.school,
                                                      color: primaryColor,
                                                      size: 30,
                                                    ),
                                                  );
                                                },
                                              ),
                                            );
                                          },
                                          loadingBuilder: (context, child,
                                              loadingProgress) {
                                            if (loadingProgress == null) {
                                              return child;
                                            }
                                            return Container(
                                              color: thirdColor,
                                              child: Center(
                                                child:
                                                    CircularProgressIndicator(
                                                  strokeWidth: 2,
                                                  valueColor:
                                                      AlwaysStoppedAnimation<
                                                          Color>(primaryColor),
                                                ),
                                              ),
                                            );
                                          },
                                        )
                                      : Container(
                                          color: thirdColor,
                                          child: Image.network(
                                            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
                                            fit: BoxFit.cover,
                                            errorBuilder:
                                                (context, error, stackTrace) {
                                              return Container(
                                                color: thirdColor,
                                                child: Icon(
                                                  Icons.school,
                                                  color: primaryColor,
                                                  size: 30,
                                                ),
                                              );
                                            },
                                          ),
                                        ),
                                ),
                              ),
                              SizedBox(width: 15),

                              Expanded(
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      university.name,
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontFamily: 'Roboto',
                                        color: Cprimary,
                                        fontWeight: FontWeight.w600,
                                      ),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    vGap(4),
                                    Text(
                                      "${university.state}, ${university.country}",
                                      style: TextStyle(
                                          fontFamily: 'Roboto',
                                          fontSize: 12,
                                          color: grey3,
                                          fontWeight: FontWeight.w600),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    vGap(15),
                                    Row(
                                      mainAxisSize: MainAxisSize.min,
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
                                          "${university.founded_year}",
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
                                      mainAxisSize: MainAxisSize.min,
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
                                            // Handle when the rating is updated
                                            print(rating);
                                          },
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                              // Action buttons
                              Container(
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    Material(
                                        type: MaterialType.transparency,
                                        child: Ink(
                                          decoration: BoxDecoration(
                                            border: Border.all(
                                                color: Colors.white,
                                                width: 2.5),
                                            color: state.loadingBookmarks
                                                    .contains(university.id)
                                                ? Colors.grey // Loading state
                                                : (state.bookmarkStates[
                                                            university.id] ??
                                                        false)
                                                    ? Colors.red // Bookmarked
                                                    : Colors
                                                        .green, // Not bookmarked
                                            shape: BoxShape.circle,
                                          ),
                                          child: InkWell(
                                            borderRadius:
                                                BorderRadius.circular(1000.0),
                                            onTap: state.loadingBookmarks
                                                    .contains(university.id)
                                                ? null // Disable tap when loading
                                                : () => notifier
                                                    .toggleBookmark(university),
                                            child: Padding(
                                              padding: EdgeInsets.all(8.0),
                                              child: state.loadingBookmarks
                                                      .contains(university.id)
                                                  ? SizedBox(
                                                      width: 16,
                                                      height: 16,
                                                      child:
                                                          CircularProgressIndicator(
                                                        strokeWidth: 2,
                                                        valueColor:
                                                            AlwaysStoppedAnimation<
                                                                    Color>(
                                                                Colors.white),
                                                      ),
                                                    )
                                                  : Icon(
                                                      (state.bookmarkStates[
                                                                  university
                                                                      .id] ??
                                                              false)
                                                          ? Icons.bookmark
                                                          : Icons
                                                              .bookmark_add_outlined,
                                                      size: 20.0,
                                                      color: Colors.white,
                                                    ),
                                            ),
                                          ),
                                        )),
                                    SizedBox(height: 25),
                                    Container(
                                      height: size?.hp(4),
                                      width: size?.wp(22),
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
                              ),
                            ],
                          );
                        },
                      ),
                    ),
                  );
                },
              ),
            ),
          ),
        );
      },
    );
  }
}
