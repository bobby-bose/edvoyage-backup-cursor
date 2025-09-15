class University {
  final int id;
  final String name;
  final String city;
  final String country;
  final String? logoUrl;
  final int? estd;
  final double? rating;
  final String? location;
  final String? logo;
  final String? banner_image;
  final String? establishedYear;
  final bool? bookmark;
  final bool? is_FMGE_affiliated;
  final bool? is_USML_affiliated;
  final bool? is_PLAB_affiliated;
  final String? about;
  final int? ranking;
  final int? founded_year;
  final int? undergraduate_programs;

  University({
    required this.id,
    required this.name,
    required this.city,
    required this.country,
    this.logoUrl,
    this.estd,
    this.rating,
    this.location,
    this.logo,
    this.banner_image,
    this.establishedYear,
    this.bookmark,
    this.is_FMGE_affiliated,
    this.is_USML_affiliated,
    this.is_PLAB_affiliated,
    this.about,
    this.ranking,
    this.founded_year,
    this.undergraduate_programs,
  });

  factory University.fromJson(Map<String, dynamic> json) {
    return University(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      city: json['city'] ?? json['location'] ?? '',
      country: json['country'] ?? '',
      logoUrl: json['logo_url'] ?? json['logo_url'],
      estd: json['estd'],
      rating: (json['rating'] ?? 0).toDouble(),
      location: json['location'],
      logo: json['logo'] ?? json['logo_url'],
      banner_image: json['banner_image'] ?? json['banner_image_url'],
      establishedYear: json['established_year'],
      bookmark: json['bookmark'],
      is_FMGE_affiliated: json['is_FMGE_affiliated'],
      is_USML_affiliated: json['is_USML_affiliated'],
      is_PLAB_affiliated: json['is_PLAB_affiliated'],
      about: json['about'],
      ranking: json['ranking'],
      founded_year: json['founded_year'],
      undergraduate_programs: json['undergraduate_programs'],
    );
  }
}
