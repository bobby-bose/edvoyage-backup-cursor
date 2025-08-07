class NotificationOffer {
  NotificationOffer({
    required this.success,
    required this.message,
    required this.data,
  });

  late final bool success;
  late final String message;
  late final List<Data> data;

  NotificationOffer.fromJson(Map<String, dynamic> json) {
    success = json['success'];
    message = json['message'];
    data = List.from(json['data']).map((e) => Data.fromJson(e)).toList();
  }

  Map<String, dynamic> toJson() {
    final result = <String, dynamic>{};
    result['success'] = success;
    result['message'] = message;
    result['data'] = data.map((e) => e.toJson()).toList();
    return result;
  }
}

class Data {
  Data({
    required this.notification_type,
    required this.content,
  });

  late final String notification_type;
  late final String content;

  Data.fromJson(Map<String, dynamic> json) {
    // check if the notification_type is present in the JSON before assigning
    notification_type = json['notification_type'] ?? '';
    content = json['content'] ?? '';
  }

  Map<String, dynamic> toJson() {
    final data = <String, dynamic>{};
    data['notification_type'] = notification_type;
    data['content'] = content;
    return data;
  }
}
