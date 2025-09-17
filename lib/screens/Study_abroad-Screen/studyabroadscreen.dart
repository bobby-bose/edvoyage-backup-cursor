import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:get/get.dart';
// Import necessary packages
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/screens/University_tabs/FeedTab.dart';
import 'package:frontend/screens/University_tabs/GalleryTab.dart';
import 'package:frontend/models/university.dart';
import 'package:frontend/screens/University_tabs/aboutTab.dart';
import 'package:frontend/screens/University_tabs/courses_screenTab.dart';
import 'package:frontend/utils/BottomNavigation/controller.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:frontend/widgets/tver_modal.dart';
import 'package:frontend/screens/WebPage/webpage.dart';

BottomNavigationController controller = Get.put(BottomNavigationController());

class UniversitHomeScreen extends StatefulWidget {
  final University university;
  const UniversitHomeScreen({super.key, required this.university});

  @override
  State<UniversitHomeScreen> createState() => _UniversitHomeScreenState();
}

class _UniversitHomeScreenState extends State<UniversitHomeScreen>
    with SingleTickerProviderStateMixin {
  TabController? _tabController;

  late University university;
  late Future<bool> userIsFollowing = Future.value(false);

  // Bookmark state management
  bool isBookmarked = false;
  bool isLoadingBookmark = false;

  @override
  void initState() {
    super.initState();
    university = widget.university;
    _tabController = TabController(length: 4, vsync: this);

    print("Checking if user follows university");
    print("Checking if user follows university");
    print("Checking if user follows university");
    print(userIsFollowing);

    // Initialize bookmark state
    isBookmarked = university.bookmark ?? false;
  }

  @override
  void dispose() {
    super.dispose();
    _tabController!.dispose();
  }

  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  Future<void> toggleBookmark() async {
    try {
      // For testing phase, use user_id = 1
      final userId = 1;

      // Show loading state immediately
      setState(() {
        isLoadingBookmark = true;
      });

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
        setState(() {
          isBookmarked = action == 'added'; // true if added, false if removed
          isLoadingBookmark = false;
        });

        print('✅ DEBUG: Bookmark toggled for university: ${university.name}');
        print('✅ DEBUG: Action: $action, New state: $isBookmarked');
      } else {
        // Clear loading state on error
        setState(() {
          isLoadingBookmark = false;
        });

        print(
            '❌ DEBUG: Failed to toggle bookmark. Status: ${response.statusCode}');
        print('❌ DEBUG: Response: ${response.body}');
      }
    } catch (e) {
      // Clear loading state on error
      setState(() {
        isLoadingBookmark = false;
      });

      print('❌ DEBUG: Error toggling bookmark: $e');
    }
  }

  double xOffset = 0;
  double yOffset = 0;
  double scaleFactor = 1;
  @override
  Widget build(BuildContext context) {
    print("🔍 DEBUG: University logo is: ${university.logo}");
    print("🔍 DEBUG: University logoUrl is: ${university.logoUrl}");
    print("🔍 DEBUG: University banner_image is: ${university.banner_image}");
    print("🔍 DEBUG: University name is: ${university.name}");
    print("🔍 DEBUG: University ID is: ${university.id}");
    print("🔍 DEBUG: University city is: ${university.city}");
    print("🔍 DEBUG: University country is: ${university.country}");

    // Debug image URLs
    final logoUrl = university.logo ?? university.logoUrl ?? '';
    final bannerUrl = university.banner_image ?? '';

    // Convert relative URLs to absolute URLs if needed
    final absoluteLogoUrl =
        logoUrl.startsWith('http') ? logoUrl : '${BaseUrl.baseUrlApi}$logoUrl';
    final absoluteBannerUrl = bannerUrl.startsWith('http')
        ? bannerUrl
        : '${BaseUrl.baseUrlApi}$bannerUrl';

    print("🔍 DEBUG: Final logo URL: $absoluteLogoUrl");
    print("🔍 DEBUG: Final banner URL: $absoluteBannerUrl");
    final labelTextStyle = Theme.of(context)
        .textTheme
        .titleSmall!
        .copyWith(fontFamily: 'Roboto', fontSize: 8.0);
    return Obx(() {
      return Scaffold(
        backgroundColor: White,
        appBar: AppBar(
          backgroundColor: White,
          centerTitle: true,
          leading: IconButton(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: Icon(Icons.arrow_back_ios, color: Cprimary)),
          title: SizedBox(
            height: 250, // Set the width of the container
            width: 200, // Set the height of the container
            child: Image.asset(
                edvoyagelogo1), // Replace with the actual image path
          ),
        ),
        body: SafeArea(
          child: Column(
            children: <Widget>[
              Stack(
                children: <Widget>[
                  // University Banner Image
                  Container(
                    width: MediaQuery.of(context).size.width,
                    height: 150.0,
                    decoration: BoxDecoration(
                      color: color3,
                      shape: BoxShape.rectangle,
                    ),
                    child: university.banner_image != null &&
                            university.banner_image!.isNotEmpty
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.network(
                              absoluteBannerUrl,
                              headers: {'User-Agent': 'Flutter App'},
                              fit: BoxFit.cover,
                              loadingBuilder:
                                  (context, child, loadingProgress) {
                                if (loadingProgress == null) return child;
                                return Container(
                                  decoration: BoxDecoration(
                                    color: color3,
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Center(
                                    child: CircularProgressIndicator(
                                      value:
                                          loadingProgress.expectedTotalBytes !=
                                                  null
                                              ? loadingProgress
                                                      .cumulativeBytesLoaded /
                                                  loadingProgress
                                                      .expectedTotalBytes!
                                              : null,
                                      color: Cprimary,
                                    ),
                                  ),
                                );
                              },
                              errorBuilder: (context, error, stackTrace) {
                                print(
                                    "🔍 DEBUG: Error loading university banner: $error");
                                print(
                                    "🔍 DEBUG: Banner URL that failed: $absoluteBannerUrl");
                                return Container(
                                  decoration: BoxDecoration(
                                    color: color3,
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Center(
                                    child: Icon(
                                      Icons.school,
                                      color: Cprimary,
                                      size: 48,
                                    ),
                                  ),
                                );
                              },
                            ),
                          )
                        : Container(
                            decoration: BoxDecoration(
                              color: color3,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Center(
                              child: Icon(
                                Icons.school,
                                color: Cprimary,
                                size: 48,
                              ),
                            ),
                          ),
                  ),
                  // University Logo
                  Align(
                    alignment: Alignment.bottomCenter,
                    heightFactor: 2.3,
                    child: Container(
                      alignment: Alignment.bottomCenter,
                      width: 100,
                      height: 90.0,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: White,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.1),
                            blurRadius: 8,
                            offset: Offset(0, 2),
                          ),
                        ],
                      ),
                      child: ClipOval(
                        child: (university.logo != null &&
                                    university.logo!.isNotEmpty) ||
                                (university.logoUrl != null &&
                                    university.logoUrl!.isNotEmpty)
                            ? Image.network(
                                absoluteLogoUrl,
                                headers: {'User-Agent': 'Flutter App'},
                                fit: BoxFit.cover,
                                loadingBuilder:
                                    (context, child, loadingProgress) {
                                  if (loadingProgress == null) return child;
                                  return Container(
                                    decoration: BoxDecoration(
                                      color: Cprimary,
                                      shape: BoxShape.circle,
                                    ),
                                    child: Center(
                                      child: CircularProgressIndicator(
                                        value: loadingProgress
                                                    .expectedTotalBytes !=
                                                null
                                            ? loadingProgress
                                                    .cumulativeBytesLoaded /
                                                loadingProgress
                                                    .expectedTotalBytes!
                                            : null,
                                        color: White,
                                      ),
                                    ),
                                  );
                                },
                                errorBuilder: (context, error, stackTrace) {
                                  print(
                                      "🔍 DEBUG: Error loading university logo: $error");
                                  print(
                                      "🔍 DEBUG: Logo URL that failed: $absoluteLogoUrl");
                                  return Container(
                                    decoration: BoxDecoration(
                                      color: Cprimary,
                                      shape: BoxShape.circle,
                                    ),
                                    child: Icon(
                                      Icons.school,
                                      color: White,
                                      size: 40,
                                    ),
                                  );
                                },
                              )
                            : Container(
                                decoration: BoxDecoration(
                                  color: Cprimary,
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(
                                  Icons.school,
                                  color: White,
                                  size: 40,
                                ),
                              ),
                      ),
                    ),
                  ),
                ],
              ),
              Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(university.name),
                      hGap(5),
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => GoogleScreenWidget(
                                      url: 'https://sibmed.ru/ru/')));
                        },
                        child: Image.asset(
                          "assets/external-link-alt.png",
                          width: 10,
                          height: 10,
                        ),
                      ),
                    ],
                  ),
                  vGap(5),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.location_on),
                      hGap(5),
                      Text(
                          '${university.location ?? ''} , ${university.country ?? ''}'),
                    ],
                  ),
                  vGap(5),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      isLoadingBookmark
                          ? ElevatedButton(
                              style: ButtonStyle(
                                  backgroundColor:
                                      WidgetStateProperty.all(Colors.grey),
                                  shape: WidgetStatePropertyAll(
                                    RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(5.0),
                                      side: BorderSide(color: grey2),
                                    ),
                                  )),
                              onPressed: null, // Disable when loading
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  SizedBox(
                                    width: 16,
                                    height: 16,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      valueColor:
                                          AlwaysStoppedAnimation<Color>(White),
                                    ),
                                  ),
                                  SizedBox(width: 8),
                                  Text(
                                    'Loading...',
                                    style: TextStyle(
                                        fontFamily: 'Roboto', color: White),
                                  ),
                                ],
                              ),
                            )
                          : isBookmarked
                              ? ElevatedButton(
                                  style: ButtonStyle(
                                      backgroundColor: WidgetStateProperty.all(
                                          secondaryColor),
                                      shape: WidgetStatePropertyAll(
                                        RoundedRectangleBorder(
                                          borderRadius:
                                              BorderRadius.circular(5.0),
                                          side: BorderSide(color: grey2),
                                        ),
                                      )),
                                  onPressed: toggleBookmark,
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Text(
                                        'UnFollow',
                                        style: TextStyle(
                                            fontFamily: 'Roboto', color: White),
                                      ),
                                      SizedBox(
                                        width: 5,
                                      ),
                                    ],
                                  ),
                                )
                              : ElevatedButton(
                                  style: ButtonStyle(
                                      backgroundColor:
                                          WidgetStateProperty.all(Ctext2),
                                      shape: WidgetStatePropertyAll(
                                        RoundedRectangleBorder(
                                          borderRadius:
                                              BorderRadius.circular(5.0),
                                          side: BorderSide(color: grey2),
                                        ),
                                      )),
                                  onPressed: toggleBookmark,
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Text(
                                        'Follow',
                                        style: TextStyle(
                                            fontFamily: 'Roboto',
                                            color: fourthColor),
                                      ),
                                      SizedBox(
                                        width: 5,
                                      ),
                                    ],
                                  ),
                                ),
                      hGap(25),
                      ElevatedButton(
                          style: ButtonStyle(
                              backgroundColor: WidgetStateProperty.all(Ctext2),
                              shape: WidgetStatePropertyAll(
                                RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(5.0),
                                  side: BorderSide(color: grey2),
                                ),
                              )),
                          onPressed: () {
                            _launchWhatsApp('1234567890');
                          },
                          child: Image.network(
                              "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/WhatsApp_icon.png/598px-WhatsApp_icon.png",
                              width: 26.0,
                              height: 26.0)),
                      hGap(25),
                      ElevatedButton(
                        style: ButtonStyle(
                            backgroundColor: WidgetStateProperty.all(Ctext2),
                            shape: WidgetStatePropertyAll(
                              RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(5.0),
                                side: BorderSide(color: grey2),
                              ),
                            )),
                        onPressed: () {
                          displayModalBottomSheet(context);
                        },
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              'Apply',
                              style: TextStyle(
                                  fontFamily: 'Roboto', color: fourthColor),
                            ),
                            SizedBox(
                              width: 5,
                            ),
                          ],
                        ),
                      ),
                    ],
                  )
                ],
              ),
              vGap(5),
              Container(
                color: White,
                child: TabBar(
                  unselectedLabelColor: Colors.grey,
                  labelColor: Cprimary,
                  controller: _tabController,
                  indicatorColor: Cprimary,
                  labelStyle: Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.copyWith(fontSize: 15.0) ??
                      TextStyle(fontSize: 15.0),
                  unselectedLabelStyle: Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.copyWith(fontSize: 14.0) ??
                      TextStyle(fontSize: 14.0),
                  indicatorSize: TabBarIndicatorSize.tab,
                  tabs: const [
                    Tab(child: Text('About')),
                    Tab(child: Text('Feed')),
                    Tab(child: Text('Courses')),
                    Tab(child: Text('Gallery')),
                  ],
                ),
              ),
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: [
                    AboutTab(university: university),
                    FeedTab(universityId: university.id),
                    CoursesScreenTab(universityId: university.id),
                    GalleryTab(universityId: university.id),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
    });
  }

  void _launchWhatsApp(String phone) async {
    Uri url = Uri.parse("https://wa.me/$phone");
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  _launchURL() async {
    const url = 'https://www.google.com';
    if (await canLaunch(url)) {
      await launch(url, forceWebView: true);
    } else {
      throw 'Could not launch $url';
    }
  }
}

Future<bool> _requestStoragePermission() async {
  var status = await Permission.storage.request();
  if (status.isGranted) {
    // Permission is granted
    return true;
  } else {
    // Permission is denied
    // Handle the denial
    return false;
  }
}

void displayModalBottomSheet(context) {
  showModalBottomSheet(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(30.0),
          topRight: Radius.circular(30.0),
          bottomLeft: Radius.circular(20.0),
          bottomRight: Radius.circular(20.0),
        ),
      ),
      isScrollControlled: true,
      context: context,
      builder: (BuildContext bc) {
        return Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(30),
              topRight: Radius.circular(30),
            ),
            color: whiteColor,
          ),
          // Adjust the height based on your needs, e.g., getHeight(context) / 2
          height: MediaQuery.of(context).size.height * 0.42,
          child: Column(
            children: [
              Expanded(
                child: DropDownDemo(
                  universityId: 1, // For testing purposes
                  universityName: "Test University", // For testing purposes
                ),
              ),
            ],
          ),
        );
      });
}
