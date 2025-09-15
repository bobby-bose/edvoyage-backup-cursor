import 'package:flutter/material.dart';

Widget buildExploreCoursesContent() {
  return Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      buildCourseCountContainer(universityImage, '300+', 'Universities'),
      buildCourseCountContainer(coursesImage, '30,000+', 'Courses'),
    ],
  );
}

Widget buildCourseCountContainer(Image image, String count, String label) {
  return Container();
}

Image universityImage = Image.asset('path/to/university_image.png');
Image coursesImage = Image.asset('path/to/courses_image.png');
