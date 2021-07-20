DROP DATABASE IF EXISTS `CAFE`;
create DATABASE CAFE;
use CAFE;

DROP TABLE IF EXISTS `STAFF`;
DROP TABLE IF EXISTS `STAFF_ASSOCIATES`;
DROP TABLE IF EXISTS `CHEF`;
DROP TABLE IF EXISTS `WAITER`;
DROP TABLE IF EXISTS `SALARY`;
DROP TABLE IF EXISTS `MENU`;
DROP TABLE IF EXISTS `CUSTOMER`;
DROP TABLE IF EXISTS `ORDERS`;
DROP TABLE IF EXISTS `COMPLETE_INFO`;
DROP TABLE IF EXISTS `PAYMENT`;

CREATE TABLE `STAFF`(
	STAFF_ID BIGINT NOT NULL,
	FNAME VARCHAR(30) NOT NULL,
	LNAME VARCHAR(30),
	EMAIL VARCHAR(50),
	ADDRESS VARCHAR(50),
	SEX VARCHAR(10),
	DOB VARCHAR(20),
	CATEGORY BIGINT,
	PRIMARY KEY(`STAFF_ID`)
);

CREATE TABLE `STAFF_CONTACT`(
	STAFF_ID BIGINT NOT NULL,
	CONTACT_NUMBER BIGINT,
	FOREIGN KEY(`STAFF_ID`) REFERENCES `STAFF`(`STAFF_ID`)
);

CREATE TABLE `STAFF_ASSOCIATES`(
	STAFF_ID BIGINT NOT NULL,
	FNAME VARCHAR(30) NOT NULL,
	LNAME VARCHAR(30),
	ADDRESS VARCHAR(50),
	CONTACT_NUMBER BIGINT NOT NULL,
	FOREIGN KEY(`STAFF_ID`) REFERENCES `STAFF`(`STAFF_ID`)	
);

CREATE TABLE `CHEF`(
	STAFF_ID BIGINT NOT NULL,
	WORK_EXPERIENCE BIGINT,
	FOREIGN KEY(`STAFF_ID`) REFERENCES `STAFF`(`STAFF_ID`)
);

CREATE TABLE `WAITER`(
	STAFF_ID BIGINT NOT NULL,
	LANGUAGE VARCHAR(20),
	FOREIGN KEY(`STAFF_ID`) REFERENCES `STAFF`(`STAFF_ID`)
);

CREATE TABLE `SALARY`(
	STAFF_ID BIGINT NOT NULL,
	BASE_SALARY BIGINT NOT NULL,
	BONUS BIGINT,
	DEDUCTIONS BIGINT,
	PRIMARY KEY(`STAFF_ID`)
);

CREATE TABLE `MENU`(
	FOOD_ID BIGINT NOT NULL,
	NAME VARCHAR(20) NOT NULL,
	ABOUT VARCHAR(50) NOT NULL,
	PRICE REAL NOT NULL,
	NO_OF_TIMES_ORDERED BIGINT NOT NULL,
	RATING REAL,
	PRIMARY KEY(`FOOD_ID`)
);

CREATE TABLE `FOOD_CATEGORY`(
	FOOD_ID BIGINT NOT NULL,
	CATEGORY VARCHAR(30),
	FOREIGN KEY(`FOOD_ID`) REFERENCES `MENU`(`FOOD_ID`)
);

CREATE TABLE `CUSTOMER`(
	CUSTOMER_ID BIGINT NOT NULL,
	FNAME VARCHAR(30) NOT NULL,
	LNAME VARCHAR(30),
	CONTACT_NUMBER BIGINT NOT NULL,
	PRIMARY KEY(`CUSTOMER_ID`)
);

CREATE TABLE `COMPLETE_INFO`(
	INVOICE_ID BIGINT NOT NULL,
	CUSTOMER_ID BIGINT NOT NULL,
	TABLE_NUMBER BIGINT NOT NULL,
	TIME_OF_DAY TIME,
	TOTAL_AMOUNT REAL NOT NULL,
	STATUS VARCHAR(20),
	PRIMARY KEY(`INVOICE_ID`),
	FOREIGN KEY(`CUSTOMER_ID`) REFERENCES `CUSTOMER`(`CUSTOMER_ID`)
);

CREATE TABLE `ORDERS`(
	ORDER_ID BIGINT NOT NULL,
	INVOICE_ID BIGINT NOT NULL,
	FOOD_ID BIGINT NOT NULL,
	STAFF_ID BIGINT NOT NULL,
	DISCOUNT BIGINT,
	QUANTITY BIGINT,
	RATING BIGINT,
	PRIMARY KEY(`ORDER_ID`),
	FOREIGN KEY(`STAFF_ID`) REFERENCES `CHEF`(`STAFF_ID`),
	FOREIGN KEY(`INVOICE_ID`) REFERENCES `COMPLETE_INFO`(`INVOICE_ID`)
);


CREATE TABLE `PAYMENT`(
	PAYMENT_ID BIGINT NOT NULL,
	INVOICE_ID BIGINT NOT NULL,
	AMOUNT REAL NOT NULL,
	PORTAL VARCHAR(50),
	PRIMARY KEY(`PAYMENT_ID`),
	FOREIGN KEY(`INVOICE_ID`) REFERENCES `COMPLETE_INFO`(`INVOICE_ID`)
);

CREATE TABLE `SERVING`(
	STAFF_ID BIGINT NOT NULL,
	ORDER_ID BIGINT NOT NULL,
	FOREIGN KEY(`STAFF_ID`) REFERENCES `WAITER`(`STAFF_ID`),
	FOREIGN KEY(`ORDER_ID`) REFERENCES `ORDERS`(`ORDER_ID`)
);

CREATE TABLE `PREPARING`(
	STAFF_ID BIGINT NOT NULL,
	ORDER_ID BIGINT NOT NULL,
	FOREIGN KEY(`STAFF_ID`) REFERENCES `CHEF`(`STAFF_ID`),
	FOREIGN KEY(`ORDER_ID`) REFERENCES `ORDERS`(`ORDER_ID`)
);

CREATE TABLE `MANAGES`(
	MANAGER_ID BIGINT NOT NULL,
	STAFF_ID BIGINT NOT NULL,
	FOREIGN KEY(`MANAGER_ID`) REFERENCES `STAFF`(`STAFF_ID`),
	FOREIGN KEY(`STAFF_ID`) REFERENCES `STAFF`(`STAFF_ID`)
);

CREATE TABLE `ORDERING`(
	CUSTOMER_ID BIGINT NOT NULL,
	ORDER_ID BIGINT,
	FOREIGN KEY(`CUSTOMER_ID`) REFERENCES `CUSTOMER`(`CUSTOMER_ID`),
	FOREIGN KEY(`ORDER_ID`) REFERENCES `ORDERS`(`ORDER_ID`)
);

CREATE TABLE `GENERATING_EINVOICE`(
	CUSTOMER_ID BIGINT NOT NULL,
	INVOICE_ID BIGINT NOT NULL,
	PAYMENT_ID BIGINT NOT NULL,
	ORDER_ID BIGINT NOT NULL,
	FOREIGN KEY(`CUSTOMER_ID`) REFERENCES `CUSTOMER`(`CUSTOMER_ID`),
	FOREIGN KEY(`INVOICE_ID`) REFERENCES `COMPLETE_INFO`(`INVOICE_ID`),
	FOREIGN KEY(`PAYMENT_ID`) REFERENCES `PAYMENT`(`PAYMENT_ID`),
	FOREIGN KEY(`ORDER_ID`) REFERENCES `ORDERS`(`ORDER_ID`)
);


INSERT INTO `MENU` VALUES (1, 'Pizza','Fresh oven baked cheese pizza', 300.0 , 10 , 47);
INSERT INTO `MENU` VALUES (2, 'Tomato Pasta', 'tasty tangy tomato flavoured pasta', 200.0 , 7 ,30);
INSERT INTO `MENU` VALUES (3, 'Winger Burger','Burger so good you\'ll be licking your fingers', 100 , 8 , 40);
INSERT INTO `MENU` VALUES (4, 'Lemonade','Refreshes your mind and soul', 150.0, 20 , 96);
INSERT INTO `MENU` VALUES (5, 'Coca Cola','Can\'t say no to Coke, Can you??', 35.0, 34 , 135);

INSERT INTO `FOOD_CATEGORY` VALUES (1,'ITALIAN');
INSERT INTO `FOOD_CATEGORY` VALUES (2,'ITALIAN');
INSERT INTO `FOOD_CATEGORY` VALUES (3,'BURGERS');
INSERT INTO `FOOD_CATEGORY` VALUES (4,'REFRESHMENT');
INSERT INTO `FOOD_CATEGORY` VALUES (5,'DRINK');
INSERT INTO `FOOD_CATEGORY` VALUES (4,'DRINK');

INSERT INTO `STAFF` VALUES (1, 'SIMON', 'BAKER','simon7@gmail.com','Tex Lane, LA','M','27-11-1990',0);
INSERT INTO `STAFF` VALUES (2, 'STEVE', 'ROGERS', 'stevie@yahoo.com','Queens, NY','M','14-12-1985',1);
INSERT INTO `STAFF` VALUES (3, 'TONY', 'STARK', 'anthony@yahoo.com','10880, Malibu Point, Cal','M','29-05-1970',1);
INSERT INTO `STAFF` VALUES (4, 'SHARON', 'CARTER', 'sharonC@gmail.com','Water Bridge, Manhattan','F','07-09-1982',2);

INSERT INTO `MANAGES` VALUES(4,1);
INSERT INTO `MANAGES` VALUES(4,2);
INSERT INTO `MANAGES` VALUES(4,3);

INSERT INTO `STAFF_CONTACT` VALUES (1,9876543210);
INSERT INTO `STAFF_CONTACT` VALUES (2,1234567890);
INSERT INTO `STAFF_CONTACT` VALUES (1,7410258963);
INSERT INTO `STAFF_CONTACT` VALUES (3,9874563210);

INSERT INTO `STAFF_ASSOCIATES` VALUES (3,'PEPPER', 'POTTS','Capitol Hill, DC', '2587413690' );
INSERT INTO `STAFF_ASSOCIATES` VALUES (2,'PEGGY', 'CARTER','Brooklyn, NY', '8496113690' );
INSERT INTO `STAFF_ASSOCIATES` VALUES (1,'TERESA', 'LISBON','San Diego', '8474859610' );

INSERT INTO `CHEF` VALUES (1, 4);

INSERT INTO `WAITER` VALUES (2, 'ENGLISH');
INSERT INTO `WAITER` VALUES (2, 'FRENCH');
INSERT INTO `WAITER` VALUES (3, 'ENGLISH');

INSERT INTO `SALARY` VALUES (1, 30000, 0, 20);
INSERT INTO `SALARY` VALUES (2, 25000, 50, 0);
INSERT INTO `SALARY` VALUES (3, 20000, 0, 0);

INSERT INTO `CUSTOMER` VALUES (1,'NICK','FURY',1000000000);
INSERT INTO `CUSTOMER` VALUES (2,'BRUCE','WAYNE',1111111111);

