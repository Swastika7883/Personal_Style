-- PostgreSQL-compatible SQL Dump
-- Converted from MySQL

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Table structure for table `outfits`
--

CREATE TABLE outfits (
    id SERIAL PRIMARY KEY,
    api_item_id VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    base_color VARCHAR(50) NOT NULL,
    undertone_match VARCHAR(50),
    image_url VARCHAR(500) NOT NULL,
    details_url VARCHAR(500),
    price NUMERIC(10,2)
);

--
-- Dumping data for table `outfits`
--

INSERT INTO outfits (id, api_item_id, category, base_color, undertone_match, image_url, details_url, price) VALUES
(52, 'caaecb1d21861f8f453da50c70b0cd9fd87a5736f40772367ce80db6a0fd3f93', 'Dress', 'beige', 'Neutral Undertone', 'https://i.pinimg.com/1200x/c5/22/96/c522961ccb0c8b7bc8df0f348b3c6b29.jpg', 'https://m.media-amazon.com/images/I/51wryt7KjjL._AC_UY1000_.jpg', NULL),
(53, 'cf5108f9ceb79a23ff496ad39ec893f44d741772373d616294250444de36b4a4', 'Dress', 'beige', 'Neutral Undertone', 'https://i.pinimg.com/1200x/5a/d2/ee/5ad2ee82f77b52b2dd4d1f078a9386e2.jpg', 'https://m.media-amazon.com/images/I/71JmoCT8b5L._AC_UY1000_.jpg', NULL),
(54, '91db5b0dbf07f6dfc2a64c5352761d069f68b28e1b73f277bbb9e1f4f6fc1e24', 'Dress', 'green', 'Neutral Undertone', 'https://i.pinimg.com/1200x/01/b3/7d/01b37d617f72061d61e6f74cd637e4fa.jpg', 'https://m.media-amazon.com/images/I/71NEyDLx2pL._AC_UF894,1000_QL80_.jpg', NULL),
(55, '4221cb1d64643f840ec302b8e94c508da213b898ee80bf5920fc17e26899d99f', 'Dress', 'green', 'Neutral Undertone', 'https://i.pinimg.com/736x/05/81/be/0581be35703905498f6c60479d4b3f44.jpg', 'https://m.media-amazon.com/images/I/71NEyDLx2pL.jpg', NULL),
(56, '0625aa2183b3cf87345777830ec239517ee5ac7d0ad6a70eee594316d897c0c7', 'Dress', 'blue', 'Neutral Undertone', 'https://i.pinimg.com/1200x/67/d0/93/67d093e52d4cc2057c2fa2f5b8ac9285.jpg', 'https://m.media-amazon.com/images/I/61YEP0PgyzL._AC_UY1000_.jpg', NULL),
(57, '4b15953181859ca1e259d05d113c8c10521488f64131004bee7f4bf9766b0afa', 'Dress', 'blue', 'Neutral Undertone', 'https://i.pinimg.com/1200x/7f/c2/c8/7fc2c847a2a89a025f633af05312b0f5.jpg', 'https://m.media-amazon.com/images/I/61m4OV6DK7L.jpg', NULL),
(58, 'd44573c6bcf895cec052403f918970fafd9ba45a821dfdccd30492d86ec880cd', 'Dress', 'white', 'Cool Undertone', 'https://i.pinimg.com/1200x/8a/b6/04/8ab604f6b31a0cd69229f2b6ef25fd13.jpg', 'https://m.media-amazon.com/images/I/61mqckw3e7L._AC_UY1000_.jpg', NULL),
(59, 'bb709ef950b6819f188e6d04db9d50c42ce6627911f787519ea0a779de6ad8d7', 'Dress', 'white', 'Cool Undertone', 'https://i.pinimg.com/1200x/db/6e/9c/db6e9cf5e703470e85624f47dc8245d7.jpg', 'https://m.media-amazon.com/images/I/51D2ibUeMhL._AC_UY1000_.jpg', NULL),
(60, '84726ee84554727524524f14cfe09f95176e95682d933d15ad9e051109999e07', 'Dress', 'gray', 'Cool Undertone', 'https://www.sunnderly.com/cdn/shop/files/file_1ea4975836_original_fc190ac5-b1f3-4a03-8df0-1dee896675ce.jpg?v=1742907057&width=900', 'https://m.media-amazon.com/images/I/515dBy6cncL._AC_UY1000_.jpg', NULL),
(61, '0a6a19b7819773e9303c8bc34d1c7561c1fc909b7d54580df97ba91f55314a6a', 'Dress', 'gray', 'Cool Undertone', 'https://i.pinimg.com/736x/03/1c/49/031c499def053f2aeea7f023f707ecf5.jpg', 'https://m.media-amazon.com/images/I/81fWUW0dlRL._AC_UF1000,1000_QL80_.jpg', NULL),
(62, '5f5a7dc974b40a49875f08ce2cd8e2cd281217604113e0c038a4b78ec9bb9beb', 'Dress', 'charcoal', 'Cool Undertone', 'https://i.pinimg.com/736x/00/51/f6/0051f617f56726fa48e8e319bbe8c679.jpg', 'https://m.media-amazon.com/images/I/710oToozRSL._AC_UY1000_.jpg', NULL),
(63, '0e3fdee16a3bb9ef5e8fb9149d7e393cf173bfed38685bdd65d02634ca14952b', 'Dress', 'charcoal', 'Cool Undertone', 'https://i.pinimg.com/1200x/08/23/09/0823096d4155c3648777c427c4ab930f.jpg', 'https://m.media-amazon.com/images/I/51wHRnxqZZL._AC_UY1000_.jpg', NULL),
(64, '2d2f1c1c45415cd3417ebe30df667173750656908e4b816f167d817a791082d8', 'Dress', 'beige', 'Neutral Undertone', 'https://i.pinimg.com/736x/0a/1b/1f/0a1b1ff3a1b459c724eac28c53f9d667.jpg', 'https://m.media-amazon.com/images/I/61XJ3qja6FL._AC_UY1000_.jpg', NULL),
(65, 'c0ee789f2b9c7aad64778f481c76040ba9bdc185f6c8c7d0af7ecc88808d0db5', 'Dress', 'blue', 'Neutral Undertone', 'https://i.pinimg.com/736x/02/46/7d/02467d2127b85203a083100133b9f9f5.jpg', 'https://m.media-amazon.com/images/I/51xgzeD8HeL._AC_UY1000_.jpg', NULL),
(66, 'd45a9c3e7ffcfd9bc7a6986e925da2bb1cf3e62935340c6a71fec71dc910e98a', 'Dress', 'blue', 'Neutral Undertone', 'https://i.pinimg.com/1200x/e5/fe/c1/e5fec1dcd1bd94d44cefbdcf0da19a50.jpg', 'https://m.media-amazon.com/images/I/516i4cLc2yL.jpg', NULL),
(67, 'd60342fd830d649f1599d643d1a715378f9c380e68b31cf3f075738fc1cd703e', 'Dress', 'pink', 'Neutral Undertone', 'https://i.pinimg.com/1200x/67/e0/40/67e040fd0481cbf9adbbdd5a33d1231c.jpg', 'https://m.media-amazon.com/images/I/814naiXu00L._AC_UF350,350_QL80_.jpg', NULL),
(68, '742644c71e0db12d0a85c6bb9d049ed870251427bb99b107c9de079db668cfc3', 'Dress', 'pink', 'Neutral Undertone', 'https://i.pinimg.com/1200x/52/17/f9/5217f93d727237dfe05e6d93c2e36bcf.jpg', 'https://m.media-amazon.com/images/I/81-WcjM-iTL._AC_UF894,1000_QL80_.jpg', NULL),
(69, '096fc8397e384fbcf17e68acdbd5e1f2113f58ce9a57c890c6ffcfffcad88e77', 'Dress', 'neutral', 'Neutral Undertone', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7Ae-nsPNZkTjwIgkl-Pz2on7cf0Z00F2WFGc9FCcwgKj0Qj2VC8NguAQ&s', 'https://m.media-amazon.com/images/I/61-NuSxRwAL._AC_UF894,1000_QL80_.jpg', NULL),
(70, 'a0003efd70acef287fb0fd281cb1505cc4d358317e19848cd02e90ae5e07f751', 'Dress', 'neutral', 'Neutral Undertone', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9X2MevResGKksk8XGliZSnpqyA2t4TogAW7obKJFEOes8yIkZ8k4pUMma&s', 'https://m.media-amazon.com/images/I/61+xHUhJDBL._AC_UY1000_.jpg', NULL),
(71, '5ab2ee5f4b8e555540fe2a6a3831ba680a3f49d0009e66778fbe95cfd6631625', 'Dress', 'white', 'Cool Undertone', 'https://i.pinimg.com/1200x/c5/31/4f/c5314f41a98cf43d074c5c32d868a01b.jpg', 'https://m.media-amazon.com/images/I/61njb8OiinL._AC_UY1000_.jpg', NULL),
(72, '6153181ea783eff4099b5c053e8dd453150beb76e3e28f20aebf8c99e0fbf1a6', 'Dress', 'lavender', 'Cool Undertone', 'https://i.pinimg.com/736x/82/5a/11/825a1174e4ae866c6e92319db9d4fcff.jpg', 'https://m.media-amazon.com/images/I/51CBlqi2eCL._AC_UY1000_.jpg', NULL),
(73, 'd9456ed36d3e4d77fe563ac843a77478156eeaf46e3de2822e5764c6d662930c', 'Dress', 'lavender', 'Cool Undertone', 'https://i.pinimg.com/1200x/e9/ad/55/e9ad552df04fe57641665699cf43cfa2.jpg', 'https://m.media-amazon.com/images/I/916jvuZUo+L.jpg', NULL),
(74, '56fec690db75c44b91a8e89adb4470456c154ab9f1f7ada500592d05afff05ab', 'Dress', 'lavender', 'Cool Undertone', 'https://i.pinimg.com/736x/32/a9/bf/32a9bff4ff067abc4f572f4a2e3d8a0a.jpg', 'https://m.media-amazon.com/images/I/51lgCPRqkUL._AC_UF894,1000_QL80_.jpg', NULL),
(75, '8a852cf1fd049d3d47d401e775d8b32239ceedd49c90bc475bf82143a11eff03', 'Dress', 'yellow', 'Warm Undertone', 'https://i.pinimg.com/736x/03/6e/a1/036ea16bc068e887ec3f5a80301455b2.jpg', 'https://m.media-amazon.com/images/I/61tmI2aTtqL.jpg', NULL),
(76, 'cc99e269bda97f06a8870960f2f7f0921d75c8c47d2fece57952c9f6211fe5ac', 'Dress', 'yellow', 'Warm Undertone', 'https://i.pinimg.com/1200x/79/d1/25/79d125d0ac4d0b87f70e7a063d6deb71.jpg', 'https://static.zara.net/assets/public/d77a/a8b0/f43c4ea49a68/1364bc20305b/04043072300-p/04043072300-p.jpg?ts=1749552276280&w=744&f=auto', NULL),
(77, '775c2cea1ebc511d2e62990f0b996301c3b970d1114b2f84250fd8a7064579c0', 'Dress', 'burgundy', 'Warm Undertone', 'https://i.pinimg.com/736x/5e/3c/41/5e3c41f95f6b8014c69ab874e5e7811b.jpg', 'https://m.media-amazon.com/images/I/61DOBS8KJrL._AC_UY1000_.jpg', NULL),
(78, '89c95fe2eeecd5a7a385f2c67938a3611220e7b4a740d663978b69745912f4cc', 'Dress', 'burgundy', 'Warm Undertone', 'https://i.pinimg.com/736x/5f/40/2b/5f402bb8eba12450335fb93bb62fa47e.jpg', 'https://m.media-amazon.com/images/I/61gSLaMkb2L._AC_UY1000_.jpg', NULL),
(79, '314f1a1418b650d38c607032decf1b8f41eb2ee944df448125eb18bb16a45c36', 'Dress', 'coral', 'Warm Undertone', 'https://i.pinimg.com/1200x/f4/4f/44/f44f44dd41c8325d3a76d78c7fdf3476.jpg', 'https://m.media-amazon.com/images/I/71+2R4gL+OL._AC_UF894,1000_QL80_.jpg', NULL),
(80, 'ae385d78c4b14fb5e49f18676e032896c8a702997d97691395fae5519578a8ae', 'Dress', 'coral', 'Warm Undertone', 'https://i.pinimg.com/1200x/84/c6/39/84c639f737cc08d21ff8886c07b6a031.jpg', 'https://m.media-amazon.com/images/I/71+2R4gL+OL.jpg', NULL),
(81, '418890d0f87589371ad26257d56862f8c9dae7464fcd7074984efedd414e8c6e', 'Dress', 'orange', 'Warm Undertone', 'https://i.pinimg.com/1200x/9e/14/44/9e144401e2da11ed8ab7d95bf70dc7b9.jpg', 'https://m.media-amazon.com/images/I/91jpudJVeLL._AC_UF894,1000_QL80_.jpg', NULL),
(82, '1e1d86450419671204ede461f650f252d815652550f601be4e1a4bf233faca5d', 'Dress', 'orange', 'Warm Undertone', 'https://i.pinimg.com/1200x/d8/6f/ba/d86fba2cd8494bd67792070117595056.jpg', 'https://m.media-amazon.com/images/I/612y3GzmyfL._AC_UY1000_.jpg', NULL),
(83, '22f04d99a4074f3e1ca30e8b0c42d65f6bb96c556b0cddfbc2db371d71df4a67', 'Dress', 'gold', 'Warm Undertone', 'https://i.pinimg.com/1200x/ce/b2/f6/ceb2f62f5a3e4adc3bf9e3b560db3713.jpg', 'https://m.media-amazon.com/images/I/71vOdpydclL._AC_UF894,1000_QL80_.jpg', NULL),
(84, 'ba78c22c7b5411c4f74ff791161d599485f5a8fb86dbc301089b39ccfed73956', 'Dress', 'gold', 'Warm Undertone', 'https://i.pinimg.com/1200x/3d/6b/a4/3d6ba465edf300b3f9e8a905a5c30bf8.jpg', 'https://m.media-amazon.com/images/I/91XJrQeJIUL._AC_UF894,1000_QL80_.jpg', NULL);

--
-- Indexes for table `outfits`
--

CREATE UNIQUE INDEX ix_outfits_api_item_id ON outfits (api_item_id);
CREATE INDEX ix_outfits_id ON outfits (id);
CREATE INDEX ix_outfits_undertone_match ON outfits (undertone_match);

-- Set the sequence to continue from the highest ID
SELECT setval('outfits_id_seq', (SELECT MAX(id) FROM outfits));