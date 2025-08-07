import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:frontend/utils/colors/colors.dart';

class MCQModuleCard extends StatelessWidget {
  final Map<String, dynamic> module;
  final VoidCallback onTap;

  const MCQModuleCard({
    super.key,
    required this.module,
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
              // MCQ Icon
              Container(
                width: 80,
                height: 60,
                decoration: BoxDecoration(
                  color: primaryColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  Icons.quiz,
                  color: primaryColor,
                  size: 32,
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
                      module['title'] ?? 'Untitled Module',
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
                    // Description
                    Text(
                      module['description'] ?? 'No description available',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 12,
                        color: grey3,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 8),
                    // Stats Row
                    Row(
                      children: [
                        // Questions Count
                        Row(
                          children: [
                            Icon(
                              Icons.question_answer,
                              size: 14,
                              color: grey3,
                            ),
                            SizedBox(width: 4),
                            Text(
                              '${module['questions_count'] ?? 0} Questions',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                          ],
                        ),
                        SizedBox(width: 16),
                        // Time Limit
                        Row(
                          children: [
                            Icon(
                              Icons.timer,
                              size: 14,
                              color: grey3,
                            ),
                            SizedBox(width: 4),
                            Text(
                              module['time_limit'] ?? 'No time limit',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                          ],
                        ),
                        SizedBox(width: 16),
                        // Difficulty
                        Container(
                          padding:
                              EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: _getDifficultyColor(
                                    module['difficulty'] ?? 'Easy')
                                .withOpacity(0.1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            module['difficulty'] ?? 'Easy',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 10,
                              fontWeight: FontWeight.w500,
                              color: _getDifficultyColor(
                                  module['difficulty'] ?? 'Easy'),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              // Access Type Icon
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildAccessIcon(),
                  SizedBox(height: 8),
                  Icon(
                    Icons.arrow_forward_ios,
                    color: grey3,
                    size: 16,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getDifficultyColor(String difficulty) {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return Colors.green;
      case 'medium':
        return Colors.orange;
      case 'hard':
        return Colors.red;
      default:
        return Colors.green;
    }
  }

  Widget _buildAccessIcon() {
    final accessType = module['accessType']?.toString().toLowerCase() ?? 'free';

    if (accessType == 'premium') {
      return Row(
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
      );
    } else {
      return Row(
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
      );
    }
  }
}
