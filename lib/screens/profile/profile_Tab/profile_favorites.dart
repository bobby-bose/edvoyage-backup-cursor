import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:http/http.dart' as http;
import 'coursestabforprofile.dart';
import 'universitytabforprofile.dart';
import '../../exploreUniversity_screen/exploreUniversitiesScreen.dart';

class ProfileFevourites extends StatefulWidget {
  const ProfileFevourites({super.key});

  @override
  _ProfileFevouritesState createState() => _ProfileFevouritesState();
}

class _ProfileFevouritesState extends State<ProfileFevourites>
    with TickerProviderStateMixin {
  late TabController _tabController;
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  // State management
  int _selectedTabIndex = 0;
  bool _isSearchVisible = false;
  String _searchQuery = '';
  String _selectedSortOption = 'Recent';

  // Tab-specific state management
  final Map<int, bool> _tabSearchVisible = {0: false, 1: false};
  final Map<int, String> _tabSearchQuery = {0: '', 1: ''};
  final Map<int, String> _tabSortOption = {0: 'Recent', 1: 'Recent'};

  int universityCount = 0;
  int courseCount = 0;
  bool isLoading = false;

  // Tab data with badges
  final List<Map<String, dynamic>> _tabs = [
    {
      'title': 'University',
      'icon': Icons.school,
      'color': primaryColor,
    },
    {
      'title': 'Courses',
      'icon': Icons.book,
      'color': secondaryColor,
    },
  ];

  final List<String> _sortOptions = [
    'Recent',
    'Alphabetical',
    'Rating',
    'Popularity',
  ];

  @override
  void initState() {
    super.initState();
    fetchBookmarksCount();
    _tabController = TabController(length: 2, vsync: this);
    _animationController = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _slideAnimation = Tween<Offset>(
      begin: Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _animationController.forward();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _animationController.dispose();
    super.dispose();
  }

  void _onTabTapped(int index) {
    setState(() {
      _selectedTabIndex = index;
    });
    _tabController.animateTo(index);
  }

  void _toggleSearch() {
    setState(() {
      _isSearchVisible = !_isSearchVisible;
      if (!_isSearchVisible) {
        _searchQuery = '';
      }
    });
  }

  void _updateSearchQuery(String query) {
    setState(() {
      _searchQuery = query;
    });
  }

  void _toggleTabSearch(int tabIndex) {
    setState(() {
      _tabSearchVisible[tabIndex] = !(_tabSearchVisible[tabIndex] ?? false);
      if (!(_tabSearchVisible[tabIndex] ?? false)) {
        _tabSearchQuery[tabIndex] = '';
      }
    });
  }

  void _updateTabSearchQuery(int tabIndex, String query) {
    setState(() {
      _tabSearchQuery[tabIndex] = query;
    });
  }

  void _showSortOptions() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildSortBottomSheet(),
    );
  }

  void _showTabSortOptions(int tabIndex) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildTabSortBottomSheet(tabIndex),
    );
  }

  Widget _buildSortBottomSheet() {
    return Container(
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle
          Container(
            margin: EdgeInsets.only(top: 12, bottom: 8),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: grey1,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          // Title
          Padding(
            padding: EdgeInsets.all(20),
            child: Row(
              children: [
                Icon(Icons.sort, color: primaryColor, size: 24),
                SizedBox(width: 12),
                Text(
                  'Sort By',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: titlecolor,
                  ),
                ),
              ],
            ),
          ),
          // Sort options
          ..._sortOptions.map((option) => _buildSortOption(option)),
          SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildTabSortBottomSheet(int tabIndex) {
    return Container(
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle
          Container(
            margin: EdgeInsets.only(top: 12, bottom: 8),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: grey1,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          // Title
          Padding(
            padding: EdgeInsets.all(20),
            child: Row(
              children: [
                Icon(Icons.sort, color: _tabs[tabIndex]['color'], size: 24),
                SizedBox(width: 12),
                Text(
                  'Sort ${_tabs[tabIndex]['title']} Favorites',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: titlecolor,
                  ),
                ),
              ],
            ),
          ),
          // Sort options
          ..._sortOptions
              .map((option) => _buildTabSortOption(option, tabIndex)),
          SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildSortOption(String option) {
    final isSelected = option == _selectedSortOption;
    return GestureDetector(
      onTap: () {
        setState(() {
          _selectedSortOption = option;
        });
        Navigator.pop(context);
      },
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
        decoration: BoxDecoration(
          color: isSelected
              ? primaryColor.withValues(alpha: 0.1)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? primaryColor : Colors.transparent,
            width: 1,
          ),
        ),
        child: Row(
          children: [
            Expanded(
              child: Text(
                option,
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: 16,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                  color: isSelected ? primaryColor : titlecolor,
                ),
              ),
            ),
            if (isSelected)
              Icon(
                Icons.check_circle,
                color: primaryColor,
                size: 20,
              ),
          ],
        ),
      ),
    );
  }

  Future<void> fetchBookmarksCount() async {
    try {
      int universityCount = 0;
      int courseCount = 0;
      // 1. Fetch Universities
      final uniResponse = await http.get(
        Uri.parse("${BaseUrl.baseUrlApi}/api/v1/bookmarks/universities/"),
        headers: {'Content-Type': 'application/json'},
      );

      if (uniResponse.statusCode == 200) {
        final Map<String, dynamic> uniData = json.decode(uniResponse.body);
        if (uniData['status'] == 'success') {
          universityCount = (uniData['data'] as List).length;
          print("🎓 University Count = $universityCount");
        }
      }

      // 2. Fetch Courses
      final courseResponse = await http.get(
        Uri.parse("${BaseUrl.baseUrlApi}/api/v1/bookmarks/courses/"),
        headers: {'Content-Type': 'application/json'},
      );

      if (courseResponse.statusCode == 200) {
        final Map<String, dynamic> courseData =
            json.decode(courseResponse.body);
        if (courseData['status'] == 'success') {
          courseCount = (courseData['data'] as List).length;
          print("📘 Course Count = $courseCount");
        }
      }

      // 3. Update UI if inside a widget
      if (mounted) {
        setState(() {});
      }
    } catch (e) {
      print("❌ Error fetching bookmarks: $e");
    }
  }

  Widget _buildTabSortOption(String option, int tabIndex) {
    final isSelected = option == (_tabSortOption[tabIndex] ?? 'Recent');
    return GestureDetector(
      onTap: () {
        setState(() {
          _tabSortOption[tabIndex] = option;
        });
        Navigator.pop(context);
      },
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
        decoration: BoxDecoration(
          color: isSelected
              ? _tabs[tabIndex]['color'].withValues(alpha: 0.1)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? _tabs[tabIndex]['color'] : Colors.transparent,
            width: 1,
          ),
        ),
        child: Row(
          children: [
            Expanded(
              child: Text(
                option,
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: 16,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                  color: isSelected ? _tabs[tabIndex]['color'] : titlecolor,
                ),
              ),
            ),
            if (isSelected)
              Icon(
                Icons.check_circle,
                color: _tabs[tabIndex]['color'],
                size: 20,
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(
        color: whiteColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          // Main header row
          Row(
            children: [
              // Title with gradient
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [primaryColor, secondaryColor],
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                    ),
                  ),
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text(
                      'Favorites',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 24,
                        fontWeight: FontWeight.w700,
                        color: whiteColor,
                      ),
                    ),
                  ),
                ),
              ),
              SizedBox(width: 12),
              // Search button
              GestureDetector(
                onTap: _toggleSearch,
                child: Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: primaryColor.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    _isSearchVisible ? Icons.close : Icons.search,
                    color: primaryColor,
                    size: 24,
                  ),
                ),
              ),
              SizedBox(width: 8),
              // Sort button
              GestureDetector(
                onTap: _showSortOptions,
                child: Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: secondaryColor.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    Icons.sort,
                    color: secondaryColor,
                    size: 24,
                  ),
                ),
              ),
            ],
          ),
          // Search bar (animated)
          if (_isSearchVisible) ...[
            SizedBox(height: 16),
            AnimatedContainer(
              duration: Duration(milliseconds: 300),
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: grey1.withValues(alpha: 0.3),
                  borderRadius: BorderRadius.circular(12),
                  border:
                      Border.all(color: primaryColor.withValues(alpha: 0.3)),
                ),
                child: Row(
                  children: [
                    Icon(Icons.search, color: grey3, size: 20),
                    SizedBox(width: 12),
                    Expanded(
                      child: TextField(
                        onChanged: _updateSearchQuery,
                        decoration: InputDecoration(
                          hintText: 'Search favorites...',
                          border: InputBorder.none,
                          hintStyle: TextStyle(
                            fontFamily: 'Poppins',
                            fontSize: 14,
                            color: grey3,
                          ),
                        ),
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 14,
                          color: titlecolor,
                        ),
                      ),
                    ),
                    if (_searchQuery.isNotEmpty)
                      GestureDetector(
                        onTap: () => _updateSearchQuery(''),
                        child: Icon(Icons.clear, color: grey3, size: 20),
                      ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: _tabs.asMap().entries.map((entry) {
          int index = entry.key;
          Map<String, dynamic> tab = entry.value;
          print(tab);
          bool isSelected = index == _selectedTabIndex;

          return Expanded(
            child: GestureDetector(
              onTap: () => _onTabTapped(index),
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 2),
                decoration: BoxDecoration(
                  color: isSelected
                      ? tab['color'].withValues(alpha: 0.1)
                      : Colors.transparent,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    // Icon and badge

                    SizedBox(height: 8),
                    // Title
                    Text(
                      tab['title'],
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        fontWeight:
                            isSelected ? FontWeight.w600 : FontWeight.w400,
                        color: isSelected ? tab['color'] : grey3,
                      ),
                    ),
                    // Animated underline
                    AnimatedContainer(
                      duration: Duration(milliseconds: 300),
                      margin: EdgeInsets.only(top: 8),
                      height: 3,
                      width: isSelected ? 40 : 0,
                      decoration: BoxDecoration(
                        color: tab['color'],
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildContent() {
    return Expanded(
      child: SlideTransition(
        position: _slideAnimation,
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: TabBarView(
            controller: _tabController,
            children: [
              // University Tab
              _buildTabContent('University', Icons.school, primaryColor),
              // Courses Tab
              _buildTabContent('Courses', Icons.book, secondaryColor),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTabContent(String title, IconData icon, Color color) {
    int tabIndex = _selectedTabIndex;
    bool isSearchVisible = _tabSearchVisible[tabIndex] ?? false;
    String searchQuery = _tabSearchQuery[tabIndex] ?? '';

    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        children: [
          // Tab content header with search and filter
          Container(
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              children: [
                // Header row
                Row(
                  children: [
                    Icon(icon, color: color, size: 24),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        '$title Favorites',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: color,
                        ),
                      ),
                    ),
                    Text(
                      tabIndex == 0
                          ? '$universityCount items'
                          : '$courseCount items',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        color: grey3,
                      ),
                    ),
                    SizedBox(width: 12),
                    // Search button for this tab
                    GestureDetector(
                      onTap: () => _toggleTabSearch(tabIndex),
                      child: Container(
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: color.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(
                          isSearchVisible ? Icons.close : Icons.search,
                          color: color,
                          size: 20,
                        ),
                      ),
                    ),
                    SizedBox(width: 8),
                    // Sort button for this tab
                    GestureDetector(
                      onTap: () => _showTabSortOptions(tabIndex),
                      child: Container(
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: color.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(
                          Icons.sort,
                          color: color,
                          size: 20,
                        ),
                      ),
                    ),
                  ],
                ),
                // Search bar for this tab
                if (isSearchVisible) ...[
                  SizedBox(height: 12),
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: whiteColor,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: color.withValues(alpha: 0.3)),
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.search, color: color, size: 18),
                        SizedBox(width: 8),
                        Expanded(
                          child: TextField(
                            onChanged: (query) =>
                                _updateTabSearchQuery(tabIndex, query),
                            decoration: InputDecoration(
                              hintText: 'Search $title favorites...',
                              border: InputBorder.none,
                              hintStyle: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 12,
                              color: titlecolor,
                            ),
                          ),
                        ),
                        if (searchQuery.isNotEmpty)
                          GestureDetector(
                            onTap: () => _updateTabSearchQuery(tabIndex, ''),
                            child: Icon(Icons.clear, color: color, size: 18),
                          ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
          SizedBox(height: 16),
          // Explore Universities Button
          Container(
            width: double.infinity,
            margin: EdgeInsets.only(bottom: 16),
            child: ElevatedButton.icon(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ExploreUniversitiesScreen(),
                  ),
                );
              },
              icon: Icon(
                Icons.explore,
                color: whiteColor,
                size: 20,
              ),
              label: Text(
                'Explore $title',
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: whiteColor,
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: color,
                foregroundColor: whiteColor,
                padding: EdgeInsets.symmetric(vertical: 16, horizontal: 24),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                elevation: 2,
              ),
            ),
          ),
          // Content area
          Expanded(
            child: _selectedTabIndex == 0
                ? UniversityFavouritesPage()
                : profilecourses(),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: SafeArea(
        child: Column(
          children: [
            // Tab Bar
            _buildTabBar(),
            // Content
            _buildContent(),
          ],
        ),
      ),
      // Floating Action Button
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Add new favorite functionality
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Add to favorites functionality coming soon!'),
              backgroundColor: primaryColor,
            ),
          );
        },
        backgroundColor: primaryColor,
        child: Icon(Icons.favorite, color: whiteColor),
      ),
    );
  }
}
