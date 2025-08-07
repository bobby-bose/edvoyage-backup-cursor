import 'package:flutter/material.dart';

import 'mcqcard.dart';

Widget buildMCQList() {
  return ListView.builder(
    itemCount: 2,
    shrinkWrap: true,
    physics: NeverScrollableScrollPhysics(),
    itemBuilder: (context, index) {
      return buildMCQCard();
    },
  );
}
