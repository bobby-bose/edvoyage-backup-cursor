class MCQ {
  String question = "";
  List<String> options = [];
  int answer = 0;

  MCQ({required this.question, required this.options, required this.answer});

  MCQ.fromJson(Map<String, dynamic> json) {
    question = json['question'];
    options = json['options'].cast<String>();
    answer = json['answer'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['question'] = question;
    data['options'] = options;
    data['answer'] = answer;
    return data;
  }
}
