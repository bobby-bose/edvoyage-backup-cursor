import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:frontend/utils/colors/colors.dart';

class VideoLectureCard extends StatelessWidget {
  final Map<String, dynamic> lecture;
  final VoidCallback onTap;

  const VideoLectureCard({
    super.key,
    required this.lecture,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        decoration: BoxDecoration(
          color: whiteColor,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Row(
            children: [
              // Thumbnail Image
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.network(
                  lecture['thumbnailUrl'] ??
                      'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
                  width: 80,
                  height: 60,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      width: 80,
                      height: 60,
                      decoration: BoxDecoration(
                        color: grey3.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(
                        Icons.video_library,
                        color: grey3,
                        size: 24,
                      ),
                    );
                  },
                ),
              ),
              SizedBox(width: 16),
              // Content Section
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Title
                    Text(
                      lecture['title'] ?? 'Untitled Lecture',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: titlecolor,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 4),
                    // Doctor Name
                    Text(
                      lecture['doctor'] ?? 'Unknown Doctor',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 12,
                        color: grey3,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 8),
                    // Duration and Access Type Row
                    Row(
                      children: [
                        // Duration
                        Row(
                          children: [
                            Icon(
                              Icons.timer,
                              size: 14,
                              color: grey3,
                            ),
                            SizedBox(width: 4),
                            Text(
                              lecture['duration'] ?? '0 Min',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                          ],
                        ),
                        Spacer(),
                        // Access Type Icon
                        _buildAccessIcon(),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Builds the access type icon (Free or Premium)
  Widget _buildAccessIcon() {
    final accessType =
        lecture['accessType']?.toString().toLowerCase() ?? 'free';

    if (accessType == 'premium') {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: secondaryColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Image.asset(
                  'assets/crown.png',
                  width: 14,
                  height: 14,
                  errorBuilder: (context, error, stackTrace) {
                    return Icon(
                      Icons.workspace_premium,
                      size: 14,
                      color: secondaryColor,
                    );
                  },
                ),
                SizedBox(width: 4),
                Text(
                  'PREMIUM',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: secondaryColor,
                  ),
                ),
              ],
            ),
          ),
        ],
      );
    } else {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: primaryColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                SvgPicture.asset(
                  'assets/lock.svg',
                  width: 14,
                  height: 14,
                  colorFilter: ColorFilter.mode(primaryColor, BlendMode.srcIn),
                  placeholderBuilder: (context) => Icon(
                    Icons.lock_open,
                    size: 14,
                    color: primaryColor,
                  ),
                ),
                SizedBox(width: 4),
                Text(
                  'FREE',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: primaryColor,
                  ),
                ),
              ],
            ),
          ),
        ],
      );
    }
  }
}
