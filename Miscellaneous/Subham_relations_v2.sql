CREATE TABLE Business(
	business_id CHAR(25) PRIMARY KEY,
	name VARCHAR(50),
	neighborhood CHAR(25),
	address CHAR(100),
	city CHAR(25),
	state CHAR(2),
	postal_code CHAR(5),
	latitude FLOAT(7),
	longitude FLOAT(7),
	numCheckins INTEGER,
	reviewrating FLOAT(1),
	review_count INTEGER,
	is_open INTEGER,
	category CHAR(50)
);

CREATE TABLE Checkin(
	business_id CHAR(25) PRIMARY KEY,
	numCheckins INTEGER
);

CREATE TABLE Review(
	review_id CHAR(25) PRIMARY KEY,
	user_id CHAR(25),
	business_id CHAR(25),
	stars INTEGER,
	_date DATE,
	_text VARCHAR(500),
	useful INTEGER,
	funny INTEGER,
	cool INTEGER
);

CREATE TABLE Users(
	user_id CHAR(25) PRIMARY KEY,
	average_stars FLOAT(2),
	compliment_cool INTEGER,
	compliment_cute INTEGER,
	compliment_funny INTEGER,
	compliment_hot INTEGER,
	compliment_list INTEGER,
	compliment_more INTEGER,
	compliment_note INTEGER,
	compliment_photos INTEGER,
	compliment_plain INTEGER,
	compliment_profile INTEGER,
	compliment_writer INTEGER,
	cool INTEGER,
	fans INTEGER,
	funny INTEGER,
	name VARCHAR(25),
	review_count INTEGER,
	useful INTEGER,
	yelping_since DATE
);

CREATE TABLE has(
	business_id CHAR(25),
	review_id CHAR(25),
	PRIMARY KEY(business_id, review_id),
	FOREIGN KEY(business_id) REFERENCES Business(business_id),
	FOREIGN KEY(review_id) REFERENCES Review(review_id)
);

CREATE TABLE logs(
	business_id CHAR(25) PRIMARY KEY,
	FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

CREATE TABLE posts(
	user_id CHAR(25),
	review_id CHAR(25),
	PRIMARY KEY(user_id, review_id),
	FOREIGN KEY(user_id) REFERENCES Users(user_id),
	FOREIGN KEY(review_id) REFERENCES Review(review_id)
);
