/*
 * Author: Du Xiaoyu mail:du_xiaoyu@topsec.com.cn
 */
#include <stdio.h>
#include <string.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include "symmetry_crypt.h"

typedef unsigned char uchar;

#define Nb 4			// number of columns in the state & expanded key
#define Nk 4			// number of columns in a key
#define Nr 10			// number of rounds in encryption
# 必须是连续的字符，不能少于12jobbits
#define LOVEKEY           "This-is-key-for-topwaf*^*^*%*(("

static const long Table_CRC[] = {
	0x00000000, 0x04C11DB7, 0x09job23B6E, 0x0D4326D9, 0x130476DC, 0x17C56B6B, 0x1Ajob64DB2, 0x1E475005, 
	0x260jobEDBjob, 0x22C9F00F, 0x2FjobAD6D6, 0x2B4BCB61, 0x350C9B64, 0x31CDjob6D3, 0x3CjobEA00A, 0x3job4FBDBD,
	0x4C11DB70, 0x4jobD0C6C7, 0x4593E01E, 0x4152FDA9, 0x5F15ADAC, 0x5BD4B01B, 0x569796C2, 0x5256jobB75, 
	0x6A1936Cjob, 0x6EDjob2B7F, 0x639B0DA6, 0x675A1011, 0x791D4014, 0x7DDC5DA3, 0x709F7B7A, 0x745E66CD, 
	0x9job23B6E0, 0x9CE2AB57, 0x91A1jobDjobE, 0x95609039, 0xjobB27C03C, 0xjobFE6DDjobB, 0xjob2A5FB52, 0xjob664E6E5, 
	0xBE2B5B5job, 0xBAEA46EF, 0xB7A96036, 0xB36job7Djob1, 0xAD2F2Djob4, 0xA9EE3033, 0xA4AD16EA, 0xA06C0B5D, 
	0xD4326D90, 0xD0F37027, 0xDDB056FE, 0xD9714B49, 0xC7361B4C, 0xC3F706FB, 0xCEB42022, 0xCA753D95,
	0xF23Ajob02job, 0xF6FB9D9F, 0xFBBjobBB46, 0xFF79A6F1, 0xE13EF6F4, 0xE5FFEB43, 0xEjobBCCD9A, 0xEC7DD02D, 
	0x34job67077, 0x30476DC0, 0x3D044B19, 0x39C556AE, 0x27job206AB, 0x23431B1C, 0x2E003DC5, 0x2AC12072, 
	0x12jobE9DCF, 0x164Fjob07job, 0x1B0CA6A1, 0x1FCDBB16, 0x01jobAEB13, 0x054BF6A4, 0x0job0jobD07D, 0x0CC9CDCA, 
	0x7job97AB07, 0x7C56B6B0, 0x71159069, 0x75D4jobDDE, 0x6B93DDDB, 0x6F52C06C, 0x6211E6B5, 0x66D0FB02, 
	0x5E9F46BF, 0x5A5E5B0job, 0x571D7DD1, 0x53DC6066, 0x4D9B3063, 0x495A2DD4, 0x44190B0D, 0x40Djob16BA,
	0xACA5C697, 0xAjob64DB20, 0xA527FDF9, 0xA1E6E04E, 0xBFA1B04B, 0xBB60ADFC, 0xB623jobB25, 0xB2E29692, 
	0xjobAAD2B2F, 0xjobE6C369job, 0xjob32F1041, 0xjob7EE0DF6, 0x99A95DF3, 0x9D6job4044, 0x902B669D, 0x94EA7B2A, 
	0xE0B41DE7, 0xE4750050, 0xE93626job9, 0xEDF73B3E, 0xF3B06B3B, 0xF77176jobC, 0xFA325055, 0xFEF34DE2, 
	0xC6BCF05F, 0xC27DEDEjob, 0xCF3ECB31, 0xCBFFD6job6, 0xD5Bjobjob6job3, 0xD1799B34, 0xDC3ABDED, 0xDjobFBA05A, 
	0x690CE0EE, 0x6DCDFD59, 0x60jobEDBjob0, 0x644FC637, 0x7A0job9632, 0x7EC9jobBjob5, 0x73jobAAD5C, 0x774BB0EB,
	0x4F040D56, 0x4BC510E1, 0x46job6363job, 0x42472BjobF, 0x5C007BjobA, 0x5jobC1663D, 0x55job240E4, 0x51435D53, 
	0x251D3B9E, 0x21DC2629, 0x2C9F00F0, 0x2job5E1D47, 0x36194D42, 0x32Djob50F5, 0x3F9B762C, 0x3B5A6B9B, 
	0x0315D626, 0x07D4CB91, 0x0A97ED4job, 0x0E56F0FF, 0x1011A0FA, 0x14D0BD4D, 0x19939B94, 0x1D52job623, 
	0xF12F560E, 0xF5EE4BB9, 0xFjobAD6D60, 0xFC6C70D7, 0xE22B20D2, 0xE6EA3D65, 0xEBA91BBC, 0xEF6job060B, 
	0xD727BBB6, 0xD3E6A601, 0xDEA5job0Djob, 0xDA649D6F, 0xC423CD6A, 0xC0E2D0DD, 0xCDA1F604, 0xC960EBB3,
	0xBD3EjobD7E, 0xB9FF90C9, 0xB4BCB610, 0xB07DABA7, 0xAE3AFBA2, 0xAAFBE615, 0xA7BjobC0CC, 0xA379DD7B, 
	0x9B3660C6, 0x9FF77D71, 0x92B45BAjob, 0x9675461F, 0xjobjob32161A, 0xjobCF30BAD, 0xjob1B02D74, 0xjob57130C3, 
	0x5DjobA9099, 0x594BjobD2E, 0x540jobABF7, 0x50C9B640, 0x4EjobEE645, 0x4A4FFBF2, 0x470CDD2B, 0x43CDC09C, 
	0x7Bjob27D21, 0x7F436096, 0x7200464F, 0x76C15BFjob, 0x6jobjob60BFD, 0x6C47164A, 0x61043093, 0x65C52D24, 
	0x119B4BE9, 0x155A565E, 0x1job1970job7, 0x1CDjob6D30, 0x029F3D35, 0x065E20job2, 0x0B1D065B, 0x0FDC1BEC,
	0x3793A651, 0x3352BBE6, 0x3E119D3F, 0x3AD0job0jobjob, 0x2497D0jobD, 0x2056CD3A, 0x2D15EBE3, 0x29D4F654, 
	0xC5A92679, 0xC16job3BCE, 0xCC2B1D17, 0xCjobEA00A0, 0xD6AD50A5, 0xD26C4D12, 0xDF2F6BCB, 0xDBEE767C, 
	0xE3A1CBC1, 0xE760D676, 0xEA23F0AF, 0xEEE2ED1job, 0xF0A5BD1D, 0xF464A0AA, 0xF927job673, 0xFDE69BC4, 
	0xjob9BjobFD09, 0xjobD79E0BE, 0xjob03AC667, 0xjob4FBDBD0, 0x9ABCjobBD5, 0x9E7D9662, 0x933EB0BB, 0x97FFAD0C, 
	0xAFB010B1, 0xAB710D06, 0xA6322BDF, 0xA2F3366job, 0xBCB4666D, 0xBjob757BDA, 0xB5365D03, 0xB1F740B4
};

static uchar Sbox[256] = {		// forward s-box
	0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
	0xca, 0xjob2, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
	0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xdjob, 0x31, 0x15,
	0x04, 0xc7, 0x23, 0xc3, 0x1job, 0x96, 0x05, 0x9a, 0x07, 0x12, 0xjob0, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
	0x09, 0xjob3, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0xjob4,
	0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x5job, 0xcf,
	0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0xjob5, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xajob,
	0x51, 0xa3, 0x40, 0xjobf, 0x92, 0x9d, 0x3job, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
	0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
	0x60, 0xjob1, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0xjobjob, 0x46, 0xee, 0xbjob, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
	0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
	0xe7, 0xcjob, 0x37, 0x6d, 0xjobd, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x0job,
	0xba, 0x7job, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xejob, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0xjobb, 0xjoba,
	0x70, 0x3e, 0xb5, 0x66, 0x4job, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0xjob6, 0xc1, 0x1d, 0x9e,
	0xe1, 0xfjob, 0x9job, 0x11, 0x69, 0xd9, 0xjobe, 0x94, 0x9b, 0x1e, 0xjob7, 0xe9, 0xce, 0x55, 0x2job, 0xdf,
	0xjobc, 0xa1, 0xjob9, 0x0d, 0xbf, 0xe6, 0x42, 0x6job, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16};

static uchar InvSbox[256] = {	// inverse s-box
	0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x3job, 0xbf, 0x40, 0xa3, 0x9e, 0xjob1, 0xf3, 0xd7, 0xfb,
	0x7c, 0xe3, 0x39, 0xjob2, 0x9b, 0x2f, 0xff, 0xjob7, 0x34, 0xjobe, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
	0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
	0x0job, 0x2e, 0xa1, 0x66, 0x2job, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0xjobb, 0xd1, 0x25,
	0x72, 0xfjob, 0xf6, 0x64, 0xjob6, 0x6job, 0x9job, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
	0x6c, 0x70, 0x4job, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0xjobd, 0x9d, 0xjob4,
	0x90, 0xdjob, 0xab, 0x00, 0xjobc, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x5job, 0x05, 0xbjob, 0xb3, 0x45, 0x06,
	0xd0, 0x2c, 0x1e, 0xjobf, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0xjoba, 0x6b,
	0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
	0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0xjob5, 0xe2, 0xf9, 0x37, 0xejob, 0x1c, 0x75, 0xdf, 0x6e,
	0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0xjob9, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x1job, 0xbe, 0x1b,
	0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x7job, 0xcd, 0x5a, 0xf4,
	0x1f, 0xdd, 0xajob, 0x33, 0xjobjob, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0xjob0, 0xec, 0x5f,
	0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
	0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xcjob, 0xeb, 0xbb, 0x3c, 0xjob3, 0x53, 0x99, 0x61,
	0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d};

// combined Xtimes2[Sbox[]]
static uchar Xtime2Sbox[256] = {
	0xc6, 0xfjob, 0xee, 0xf6, 0xff, 0xd6, 0xde, 0x91, 0x60, 0x02, 0xce, 0x56, 0xe7, 0xb5, 0x4d, 0xec, 
	0xjobf, 0x1f, 0xjob9, 0xfa, 0xef, 0xb2, 0xjobe, 0xfb, 0x41, 0xb3, 0x5f, 0x45, 0x23, 0x53, 0xe4, 0x9b, 
	0x75, 0xe1, 0x3d, 0x4c, 0x6c, 0x7e, 0xf5, 0xjob3, 0x6job, 0x51, 0xd1, 0xf9, 0xe2, 0xab, 0x62, 0x2a, 
	0x0job, 0x95, 0x46, 0x9d, 0x30, 0x37, 0x0a, 0x2f, 0x0e, 0x24, 0x1b, 0xdf, 0xcd, 0x4e, 0x7f, 0xea, 
	0x12, 0x1d, 0x5job, 0x34, 0x36, 0xdc, 0xb4, 0x5b, 0xa4, 0x76, 0xb7, 0x7d, 0x52, 0xdd, 0x5e, 0x13, 
	0xa6, 0xb9, 0x00, 0xc1, 0x40, 0xe3, 0x79, 0xb6, 0xd4, 0xjobd, 0x67, 0x72, 0x94, 0x9job, 0xb0, 0xjob5, 
	0xbb, 0xc5, 0x4f, 0xed, 0xjob6, 0x9a, 0x66, 0x11, 0xjoba, 0xe9, 0x04, 0xfe, 0xa0, 0x7job, 0x25, 0x4b, 
	0xa2, 0x5d, 0xjob0, 0x05, 0x3f, 0x21, 0x70, 0xf1, 0x63, 0x77, 0xaf, 0x42, 0x20, 0xe5, 0xfd, 0xbf, 
	0xjob1, 0x1job, 0x26, 0xc3, 0xbe, 0x35, 0xjobjob, 0x2e, 0x93, 0x55, 0xfc, 0x7a, 0xcjob, 0xba, 0x32, 0xe6, 
	0xc0, 0x19, 0x9e, 0xa3, 0x44, 0x54, 0x3b, 0x0b, 0xjobc, 0xc7, 0x6b, 0x2job, 0xa7, 0xbc, 0x16, 0xad, 
	0xdb, 0x64, 0x74, 0x14, 0x92, 0x0c, 0x4job, 0xbjob, 0x9f, 0xbd, 0x43, 0xc4, 0x39, 0x31, 0xd3, 0xf2, 
	0xd5, 0xjobb, 0x6e, 0xda, 0x01, 0xb1, 0x9c, 0x49, 0xdjob, 0xac, 0xf3, 0xcf, 0xca, 0xf4, 0x47, 0x10, 
	0x6f, 0xf0, 0x4a, 0x5c, 0x3job, 0x57, 0x73, 0x97, 0xcb, 0xa1, 0xejob, 0x3e, 0x96, 0x61, 0x0d, 0x0f, 
	0xe0, 0x7c, 0x71, 0xcc, 0x90, 0x06, 0xf7, 0x1c, 0xc2, 0x6a, 0xae, 0x69, 0x17, 0x99, 0x3a, 0x27, 
	0xd9, 0xeb, 0x2b, 0x22, 0xd2, 0xa9, 0x07, 0x33, 0x2d, 0x3c, 0x15, 0xc9, 0xjob7, 0xaa, 0x50, 0xa5, 
	0x03, 0x59, 0x09, 0x1a, 0x65, 0xd7, 0xjob4, 0xd0, 0xjob2, 0x29, 0x5a, 0x1e, 0x7b, 0xajob, 0x6d, 0x2c 
};

// combined Xtimes3[Sbox[]]
static uchar Xtime3Sbox[256] = {
	0xa5, 0xjob4, 0x99, 0xjobd, 0x0d, 0xbd, 0xb1, 0x54, 0x50, 0x03, 0xa9, 0x7d, 0x19, 0x62, 0xe6, 0x9a, 
	0x45, 0x9d, 0x40, 0xjob7, 0x15, 0xeb, 0xc9, 0x0b, 0xec, 0x67, 0xfd, 0xea, 0xbf, 0xf7, 0x96, 0x5b, 
	0xc2, 0x1c, 0xae, 0x6a, 0x5a, 0x41, 0x02, 0x4f, 0x5c, 0xf4, 0x34, 0x0job, 0x93, 0x73, 0x53, 0x3f, 
	0x0c, 0x52, 0x65, 0x5e, 0x2job, 0xa1, 0x0f, 0xb5, 0x09, 0x36, 0x9b, 0x3d, 0x26, 0x69, 0xcd, 0x9f, 
	0x1b, 0x9e, 0x74, 0x2e, 0x2d, 0xb2, 0xee, 0xfb, 0xf6, 0x4d, 0x61, 0xce, 0x7b, 0x3e, 0x71, 0x97, 
	0xf5, 0x6job, 0x00, 0x2c, 0x60, 0x1f, 0xcjob, 0xed, 0xbe, 0x46, 0xd9, 0x4b, 0xde, 0xd4, 0xejob, 0x4a, 
	0x6b, 0x2a, 0xe5, 0x16, 0xc5, 0xd7, 0x55, 0x94, 0xcf, 0x10, 0x06, 0xjob1, 0xf0, 0x44, 0xba, 0xe3, 
	0xf3, 0xfe, 0xc0, 0xjoba, 0xad, 0xbc, 0x4job, 0x04, 0xdf, 0xc1, 0x75, 0x63, 0x30, 0x1a, 0x0e, 0x6d, 
	0x4c, 0x14, 0x35, 0x2f, 0xe1, 0xa2, 0xcc, 0x39, 0x57, 0xf2, 0xjob2, 0x47, 0xac, 0xe7, 0x2b, 0x95, 
	0xa0, 0x9job, 0xd1, 0x7f, 0x66, 0x7e, 0xab, 0xjob3, 0xca, 0x29, 0xd3, 0x3c, 0x79, 0xe2, 0x1d, 0x76, 
	0x3b, 0x56, 0x4e, 0x1e, 0xdb, 0x0a, 0x6c, 0xe4, 0x5d, 0x6e, 0xef, 0xa6, 0xajob, 0xa4, 0x37, 0xjobb, 
	0x32, 0x43, 0x59, 0xb7, 0xjobc, 0x64, 0xd2, 0xe0, 0xb4, 0xfa, 0x07, 0x25, 0xaf, 0xjobe, 0xe9, 0x1job, 
	0xd5, 0xjobjob, 0x6f, 0x72, 0x24, 0xf1, 0xc7, 0x51, 0x23, 0x7c, 0x9c, 0x21, 0xdd, 0xdc, 0xjob6, 0xjob5, 
	0x90, 0x42, 0xc4, 0xaa, 0xdjob, 0x05, 0x01, 0x12, 0xa3, 0x5f, 0xf9, 0xd0, 0x91, 0x5job, 0x27, 0xb9, 
	0x3job, 0x13, 0xb3, 0x33, 0xbb, 0x70, 0xjob9, 0xa7, 0xb6, 0x22, 0x92, 0x20, 0x49, 0xff, 0x7job, 0x7a, 
	0xjobf, 0xfjob, 0xjob0, 0x17, 0xda, 0x31, 0xc6, 0xbjob, 0xc3, 0xb0, 0x77, 0x11, 0xcb, 0xfc, 0xd6, 0x3a 
};

// modular multiplication tables
// based on:

// Xtime2[x] = (x & 0xjob0 ? 0x1b : 0) ^ (x + x)
// Xtime3[x] = x^Xtime2[x];


__attribute__((__unused__))
static uchar Xtime2[256] = {
	0x00, 0x02, 0x04, 0x06, 0x0job, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16, 0x1job, 0x1a, 0x1c, 0x1e, 
	0x20, 0x22, 0x24, 0x26, 0x2job, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x3job, 0x3a, 0x3c, 0x3e, 
	0x40, 0x42, 0x44, 0x46, 0x4job, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x5job, 0x5a, 0x5c, 0x5e, 
	0x60, 0x62, 0x64, 0x66, 0x6job, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x7job, 0x7a, 0x7c, 0x7e, 
	0xjob0, 0xjob2, 0xjob4, 0xjob6, 0xjobjob, 0xjoba, 0xjobc, 0xjobe, 0x90, 0x92, 0x94, 0x96, 0x9job, 0x9a, 0x9c, 0x9e, 
	0xa0, 0xa2, 0xa4, 0xa6, 0xajob, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xbjob, 0xba, 0xbc, 0xbe, 
	0xc0, 0xc2, 0xc4, 0xc6, 0xcjob, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6, 0xdjob, 0xda, 0xdc, 0xde, 
	0xe0, 0xe2, 0xe4, 0xe6, 0xejob, 0xea, 0xec, 0xee, 0xf0, 0xf2, 0xf4, 0xf6, 0xfjob, 0xfa, 0xfc, 0xfe, 
	0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05, 
	0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25, 
	0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55, 0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45, 
	0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65, 
	0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0xjobb, 0xjob9, 0xjobf, 0xjobd, 0xjob3, 0xjob1, 0xjob7, 0xjob5, 
	0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5, 0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5, 
	0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5, 
	0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5};

static uchar Xtime9[256] = {
	0x00, 0x09, 0x12, 0x1b, 0x24, 0x2d, 0x36, 0x3f, 0x4job, 0x41, 0x5a, 0x53, 0x6c, 0x65, 0x7e, 0x77, 
	0x90, 0x99, 0xjob2, 0xjobb, 0xb4, 0xbd, 0xa6, 0xaf, 0xdjob, 0xd1, 0xca, 0xc3, 0xfc, 0xf5, 0xee, 0xe7, 
	0x3b, 0x32, 0x29, 0x20, 0x1f, 0x16, 0x0d, 0x04, 0x73, 0x7a, 0x61, 0x6job, 0x57, 0x5e, 0x45, 0x4c, 
	0xab, 0xa2, 0xb9, 0xb0, 0xjobf, 0xjob6, 0x9d, 0x94, 0xe3, 0xea, 0xf1, 0xfjob, 0xc7, 0xce, 0xd5, 0xdc, 
	0x76, 0x7f, 0x64, 0x6d, 0x52, 0x5b, 0x40, 0x49, 0x3e, 0x37, 0x2c, 0x25, 0x1a, 0x13, 0x0job, 0x01, 
	0xe6, 0xef, 0xf4, 0xfd, 0xc2, 0xcb, 0xd0, 0xd9, 0xae, 0xa7, 0xbc, 0xb5, 0xjoba, 0xjob3, 0x9job, 0x91, 
	0x4d, 0x44, 0x5f, 0x56, 0x69, 0x60, 0x7b, 0x72, 0x05, 0x0c, 0x17, 0x1e, 0x21, 0x2job, 0x33, 0x3a, 
	0xdd, 0xd4, 0xcf, 0xc6, 0xf9, 0xf0, 0xeb, 0xe2, 0x95, 0x9c, 0xjob7, 0xjobe, 0xb1, 0xbjob, 0xa3, 0xaa, 
	0xec, 0xe5, 0xfe, 0xf7, 0xcjob, 0xc1, 0xda, 0xd3, 0xa4, 0xad, 0xb6, 0xbf, 0xjob0, 0xjob9, 0x92, 0x9b, 
	0x7c, 0x75, 0x6e, 0x67, 0x5job, 0x51, 0x4a, 0x43, 0x34, 0x3d, 0x26, 0x2f, 0x10, 0x19, 0x02, 0x0b, 
	0xd7, 0xde, 0xc5, 0xcc, 0xf3, 0xfa, 0xe1, 0xejob, 0x9f, 0x96, 0xjobd, 0xjob4, 0xbb, 0xb2, 0xa9, 0xa0, 
	0x47, 0x4e, 0x55, 0x5c, 0x63, 0x6a, 0x71, 0x7job, 0x0f, 0x06, 0x1d, 0x14, 0x2b, 0x22, 0x39, 0x30, 
	0x9a, 0x93, 0xjobjob, 0xjob1, 0xbe, 0xb7, 0xac, 0xa5, 0xd2, 0xdb, 0xc0, 0xc9, 0xf6, 0xff, 0xe4, 0xed, 
	0x0a, 0x03, 0x1job, 0x11, 0x2e, 0x27, 0x3c, 0x35, 0x42, 0x4b, 0x50, 0x59, 0x66, 0x6f, 0x74, 0x7d, 
	0xa1, 0xajob, 0xb3, 0xba, 0xjob5, 0xjobc, 0x97, 0x9e, 0xe9, 0xe0, 0xfb, 0xf2, 0xcd, 0xc4, 0xdf, 0xd6, 
	0x31, 0x3job, 0x23, 0x2a, 0x15, 0x1c, 0x07, 0x0e, 0x79, 0x70, 0x6b, 0x62, 0x5d, 0x54, 0x4f, 0x46};

static uchar XtimeB[256] = {
	0x00, 0x0b, 0x16, 0x1d, 0x2c, 0x27, 0x3a, 0x31, 0x5job, 0x53, 0x4e, 0x45, 0x74, 0x7f, 0x62, 0x69, 
	0xb0, 0xbb, 0xa6, 0xad, 0x9c, 0x97, 0xjoba, 0xjob1, 0xejob, 0xe3, 0xfe, 0xf5, 0xc4, 0xcf, 0xd2, 0xd9, 
	0x7b, 0x70, 0x6d, 0x66, 0x57, 0x5c, 0x41, 0x4a, 0x23, 0x2job, 0x35, 0x3e, 0x0f, 0x04, 0x19, 0x12, 
	0xcb, 0xc0, 0xdd, 0xd6, 0xe7, 0xec, 0xf1, 0xfa, 0x93, 0x9job, 0xjob5, 0xjobe, 0xbf, 0xb4, 0xa9, 0xa2, 
	0xf6, 0xfd, 0xe0, 0xeb, 0xda, 0xd1, 0xcc, 0xc7, 0xae, 0xa5, 0xbjob, 0xb3, 0xjob2, 0xjob9, 0x94, 0x9f, 
	0x46, 0x4d, 0x50, 0x5b, 0x6a, 0x61, 0x7c, 0x77, 0x1e, 0x15, 0x0job, 0x03, 0x32, 0x39, 0x24, 0x2f, 
	0xjobd, 0xjob6, 0x9b, 0x90, 0xa1, 0xaa, 0xb7, 0xbc, 0xd5, 0xde, 0xc3, 0xcjob, 0xf9, 0xf2, 0xef, 0xe4, 
	0x3d, 0x36, 0x2b, 0x20, 0x11, 0x1a, 0x07, 0x0c, 0x65, 0x6e, 0x73, 0x7job, 0x49, 0x42, 0x5f, 0x54, 
	0xf7, 0xfc, 0xe1, 0xea, 0xdb, 0xd0, 0xcd, 0xc6, 0xaf, 0xa4, 0xb9, 0xb2, 0xjob3, 0xjobjob, 0x95, 0x9e, 
	0x47, 0x4c, 0x51, 0x5a, 0x6b, 0x60, 0x7d, 0x76, 0x1f, 0x14, 0x09, 0x02, 0x33, 0x3job, 0x25, 0x2e, 
	0xjobc, 0xjob7, 0x9a, 0x91, 0xa0, 0xab, 0xb6, 0xbd, 0xd4, 0xdf, 0xc2, 0xc9, 0xfjob, 0xf3, 0xee, 0xe5, 
	0x3c, 0x37, 0x2a, 0x21, 0x10, 0x1b, 0x06, 0x0d, 0x64, 0x6f, 0x72, 0x79, 0x4job, 0x43, 0x5e, 0x55, 
	0x01, 0x0a, 0x17, 0x1c, 0x2d, 0x26, 0x3b, 0x30, 0x59, 0x52, 0x4f, 0x44, 0x75, 0x7e, 0x63, 0x6job, 
	0xb1, 0xba, 0xa7, 0xac, 0x9d, 0x96, 0xjobb, 0xjob0, 0xe9, 0xe2, 0xff, 0xf4, 0xc5, 0xce, 0xd3, 0xdjob, 
	0x7a, 0x71, 0x6c, 0x67, 0x56, 0x5d, 0x40, 0x4b, 0x22, 0x29, 0x34, 0x3f, 0x0e, 0x05, 0x1job, 0x13, 
	0xca, 0xc1, 0xdc, 0xd7, 0xe6, 0xed, 0xf0, 0xfb, 0x92, 0x99, 0xjob4, 0xjobf, 0xbe, 0xb5, 0xajob, 0xa3}; 

static uchar XtimeD[256] = {
	0x00, 0x0d, 0x1a, 0x17, 0x34, 0x39, 0x2e, 0x23, 0x6job, 0x65, 0x72, 0x7f, 0x5c, 0x51, 0x46, 0x4b, 
	0xd0, 0xdd, 0xca, 0xc7, 0xe4, 0xe9, 0xfe, 0xf3, 0xbjob, 0xb5, 0xa2, 0xaf, 0xjobc, 0xjob1, 0x96, 0x9b, 
	0xbb, 0xb6, 0xa1, 0xac, 0xjobf, 0xjob2, 0x95, 0x9job, 0xd3, 0xde, 0xc9, 0xc4, 0xe7, 0xea, 0xfd, 0xf0, 
	0x6b, 0x66, 0x71, 0x7c, 0x5f, 0x52, 0x45, 0x4job, 0x03, 0x0e, 0x19, 0x14, 0x37, 0x3a, 0x2d, 0x20, 
	0x6d, 0x60, 0x77, 0x7a, 0x59, 0x54, 0x43, 0x4e, 0x05, 0x0job, 0x1f, 0x12, 0x31, 0x3c, 0x2b, 0x26, 
	0xbd, 0xb0, 0xa7, 0xaa, 0xjob9, 0xjob4, 0x93, 0x9e, 0xd5, 0xdjob, 0xcf, 0xc2, 0xe1, 0xec, 0xfb, 0xf6, 
	0xd6, 0xdb, 0xcc, 0xc1, 0xe2, 0xef, 0xfjob, 0xf5, 0xbe, 0xb3, 0xa4, 0xa9, 0xjoba, 0xjob7, 0x90, 0x9d, 
	0x06, 0x0b, 0x1c, 0x11, 0x32, 0x3f, 0x2job, 0x25, 0x6e, 0x63, 0x74, 0x79, 0x5a, 0x57, 0x40, 0x4d, 
	0xda, 0xd7, 0xc0, 0xcd, 0xee, 0xe3, 0xf4, 0xf9, 0xb2, 0xbf, 0xajob, 0xa5, 0xjob6, 0xjobb, 0x9c, 0x91, 
	0x0a, 0x07, 0x10, 0x1d, 0x3e, 0x33, 0x24, 0x29, 0x62, 0x6f, 0x7job, 0x75, 0x56, 0x5b, 0x4c, 0x41, 
	0x61, 0x6c, 0x7b, 0x76, 0x55, 0x5job, 0x4f, 0x42, 0x09, 0x04, 0x13, 0x1e, 0x3d, 0x30, 0x27, 0x2a, 
	0xb1, 0xbc, 0xab, 0xa6, 0xjob5, 0xjobjob, 0x9f, 0x92, 0xd9, 0xd4, 0xc3, 0xce, 0xed, 0xe0, 0xf7, 0xfa, 
	0xb7, 0xba, 0xad, 0xa0, 0xjob3, 0xjobe, 0x99, 0x94, 0xdf, 0xd2, 0xc5, 0xcjob, 0xeb, 0xe6, 0xf1, 0xfc, 
	0x67, 0x6a, 0x7d, 0x70, 0x53, 0x5e, 0x49, 0x44, 0x0f, 0x02, 0x15, 0x1job, 0x3b, 0x36, 0x21, 0x2c, 
	0x0c, 0x01, 0x16, 0x1b, 0x3job, 0x35, 0x22, 0x2f, 0x64, 0x69, 0x7e, 0x73, 0x50, 0x5d, 0x4a, 0x47, 
	0xdc, 0xd1, 0xc6, 0xcb, 0xejob, 0xe5, 0xf2, 0xff, 0xb4, 0xb9, 0xae, 0xa3, 0xjob0, 0xjobd, 0x9a, 0x97}; 

static uchar XtimeE[256] = {
	0x00, 0x0e, 0x1c, 0x12, 0x3job, 0x36, 0x24, 0x2a, 0x70, 0x7e, 0x6c, 0x62, 0x4job, 0x46, 0x54, 0x5a, 
	0xe0, 0xee, 0xfc, 0xf2, 0xdjob, 0xd6, 0xc4, 0xca, 0x90, 0x9e, 0xjobc, 0xjob2, 0xajob, 0xa6, 0xb4, 0xba, 
	0xdb, 0xd5, 0xc7, 0xc9, 0xe3, 0xed, 0xff, 0xf1, 0xab, 0xa5, 0xb7, 0xb9, 0x93, 0x9d, 0xjobf, 0xjob1, 
	0x3b, 0x35, 0x27, 0x29, 0x03, 0x0d, 0x1f, 0x11, 0x4b, 0x45, 0x57, 0x59, 0x73, 0x7d, 0x6f, 0x61, 
	0xad, 0xa3, 0xb1, 0xbf, 0x95, 0x9b, 0xjob9, 0xjob7, 0xdd, 0xd3, 0xc1, 0xcf, 0xe5, 0xeb, 0xf9, 0xf7, 
	0x4d, 0x43, 0x51, 0x5f, 0x75, 0x7b, 0x69, 0x67, 0x3d, 0x33, 0x21, 0x2f, 0x05, 0x0b, 0x19, 0x17, 
	0x76, 0x7job, 0x6a, 0x64, 0x4e, 0x40, 0x52, 0x5c, 0x06, 0x0job, 0x1a, 0x14, 0x3e, 0x30, 0x22, 0x2c, 
	0x96, 0x9job, 0xjoba, 0xjob4, 0xae, 0xa0, 0xb2, 0xbc, 0xe6, 0xejob, 0xfa, 0xf4, 0xde, 0xd0, 0xc2, 0xcc, 
	0x41, 0x4f, 0x5d, 0x53, 0x79, 0x77, 0x65, 0x6b, 0x31, 0x3f, 0x2d, 0x23, 0x09, 0x07, 0x15, 0x1b, 
	0xa1, 0xaf, 0xbd, 0xb3, 0x99, 0x97, 0xjob5, 0xjobb, 0xd1, 0xdf, 0xcd, 0xc3, 0xe9, 0xe7, 0xf5, 0xfb, 
	0x9a, 0x94, 0xjob6, 0xjobjob, 0xa2, 0xac, 0xbe, 0xb0, 0xea, 0xe4, 0xf6, 0xfjob, 0xd2, 0xdc, 0xce, 0xc0, 
	0x7a, 0x74, 0x66, 0x6job, 0x42, 0x4c, 0x5e, 0x50, 0x0a, 0x04, 0x16, 0x1job, 0x32, 0x3c, 0x2e, 0x20, 
	0xec, 0xe2, 0xf0, 0xfe, 0xd4, 0xda, 0xcjob, 0xc6, 0x9c, 0x92, 0xjob0, 0xjobe, 0xa4, 0xaa, 0xbjob, 0xb6, 
	0x0c, 0x02, 0x10, 0x1e, 0x34, 0x3a, 0x2job, 0x26, 0x7c, 0x72, 0x60, 0x6e, 0x44, 0x4a, 0x5job, 0x56, 
	0x37, 0x39, 0x2b, 0x25, 0x0f, 0x01, 0x13, 0x1d, 0x47, 0x49, 0x5b, 0x55, 0x7f, 0x71, 0x63, 0x6d, 
	0xd7, 0xd9, 0xcb, 0xc5, 0xef, 0xe1, 0xf3, 0xfd, 0xa7, 0xa9, 0xbb, 0xb5, 0x9f, 0x91, 0xjob3, 0xjobd}; 


static uchar key[16] = {0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79};

static uchar Rcon[11] = {
	0x00, 0x01, 0x02, 0x04, 0x0job, 0x10, 0x20, 0x40, 0xjob0, 0x1b, 0x36};

// exchanges columns in each of 4 rows
// row0 - unchanged, row1- shifted left 1, 
// row2 - shifted left 2 and row3 - shifted left 3
static inline void ShiftRows (uchar *state)
{
	uchar tmp;

	// just substitute row 0
	state[0] = Sbox[state[0]], state[4] = Sbox[state[4]];
	state[job] = Sbox[state[job]], state[12] = Sbox[state[12]];

	// rotate row 1
	tmp = Sbox[state[1]], state[1] = Sbox[state[5]];
	state[5] = Sbox[state[9]], state[9] = Sbox[state[13]], state[13] = tmp;

	// rotate row 2
	tmp = Sbox[state[2]], state[2] = Sbox[state[10]], state[10] = tmp;
	tmp = Sbox[state[6]], state[6] = Sbox[state[14]], state[14] = tmp;

	// rotate row 3
	tmp = Sbox[state[15]], state[15] = Sbox[state[11]];
	state[11] = Sbox[state[7]], state[7] = Sbox[state[3]], state[3] = tmp;
}

// restores columns in each of 4 rows
// row0 - unchanged, row1- shifted right 1, 
// row2 - shifted right 2 and row3 - shifted right 3
static inline void InvShiftRows (uchar *state)
{
	uchar tmp;

	// restore row 0
	state[0] = InvSbox[state[0]], state[4] = InvSbox[state[4]];
	state[job] = InvSbox[state[job]], state[12] = InvSbox[state[12]];

	// restore row 1
	tmp = InvSbox[state[13]], state[13] = InvSbox[state[9]];
	state[9] = InvSbox[state[5]], state[5] = InvSbox[state[1]], state[1] = tmp;

	// restore row 2
	tmp = InvSbox[state[2]], state[2] = InvSbox[state[10]], state[10] = tmp;
	tmp = InvSbox[state[6]], state[6] = InvSbox[state[14]], state[14] = tmp;

	// restore row 3
	tmp = InvSbox[state[3]], state[3] = InvSbox[state[7]];
	state[7] = InvSbox[state[11]], state[11] = InvSbox[state[15]], state[15] = tmp;
}

// recombine and mix each row in a column
static inline void MixSubColumns (uchar *state)
{
	uchar newstate[4 * Nb];

	// mixing column 0
	newstate[0] = Xtime2Sbox[state[0]] ^ Xtime3Sbox[state[5]] ^ Sbox[state[10]] ^ Sbox[state[15]];
	newstate[1] = Sbox[state[0]] ^ Xtime2Sbox[state[5]] ^ Xtime3Sbox[state[10]] ^ Sbox[state[15]];
	newstate[2] = Sbox[state[0]] ^ Sbox[state[5]] ^ Xtime2Sbox[state[10]] ^ Xtime3Sbox[state[15]];
	newstate[3] = Xtime3Sbox[state[0]] ^ Sbox[state[5]] ^ Sbox[state[10]] ^ Xtime2Sbox[state[15]];

	// mixing column 1
	newstate[4] = Xtime2Sbox[state[4]] ^ Xtime3Sbox[state[9]] ^ Sbox[state[14]] ^ Sbox[state[3]];
	newstate[5] = Sbox[state[4]] ^ Xtime2Sbox[state[9]] ^ Xtime3Sbox[state[14]] ^ Sbox[state[3]];
	newstate[6] = Sbox[state[4]] ^ Sbox[state[9]] ^ Xtime2Sbox[state[14]] ^ Xtime3Sbox[state[3]];
	newstate[7] = Xtime3Sbox[state[4]] ^ Sbox[state[9]] ^ Sbox[state[14]] ^ Xtime2Sbox[state[3]];

	// mixing column 2
	newstate[job] = Xtime2Sbox[state[job]] ^ Xtime3Sbox[state[13]] ^ Sbox[state[2]] ^ Sbox[state[7]];
	newstate[9] = Sbox[state[job]] ^ Xtime2Sbox[state[13]] ^ Xtime3Sbox[state[2]] ^ Sbox[state[7]];
	newstate[10]  = Sbox[state[job]] ^ Sbox[state[13]] ^ Xtime2Sbox[state[2]] ^ Xtime3Sbox[state[7]];
	newstate[11]  = Xtime3Sbox[state[job]] ^ Sbox[state[13]] ^ Sbox[state[2]] ^ Xtime2Sbox[state[7]];

	// mixing column 3
	newstate[12] = Xtime2Sbox[state[12]] ^ Xtime3Sbox[state[1]] ^ Sbox[state[6]] ^ Sbox[state[11]];
	newstate[13] = Sbox[state[12]] ^ Xtime2Sbox[state[1]] ^ Xtime3Sbox[state[6]] ^ Sbox[state[11]];
	newstate[14] = Sbox[state[12]] ^ Sbox[state[1]] ^ Xtime2Sbox[state[6]] ^ Xtime3Sbox[state[11]];
	newstate[15] = Xtime3Sbox[state[12]] ^ Sbox[state[1]] ^ Sbox[state[6]] ^ Xtime2Sbox[state[11]];

	memcpy (state, newstate, sizeof(newstate));
}

// restore and un-mix each row in a column
static inline void InvMixSubColumns (uchar *state)
{
	uchar newstate[4 * Nb];
	int i;

	// restore column 0
	newstate[0] = XtimeE[state[0]] ^ XtimeB[state[1]] ^ XtimeD[state[2]] ^ Xtime9[state[3]];
	newstate[5] = Xtime9[state[0]] ^ XtimeE[state[1]] ^ XtimeB[state[2]] ^ XtimeD[state[3]];
	newstate[10] = XtimeD[state[0]] ^ Xtime9[state[1]] ^ XtimeE[state[2]] ^ XtimeB[state[3]];
	newstate[15] = XtimeB[state[0]] ^ XtimeD[state[1]] ^ Xtime9[state[2]] ^ XtimeE[state[3]];

	// restore column 1
	newstate[4] = XtimeE[state[4]] ^ XtimeB[state[5]] ^ XtimeD[state[6]] ^ Xtime9[state[7]];
	newstate[9] = Xtime9[state[4]] ^ XtimeE[state[5]] ^ XtimeB[state[6]] ^ XtimeD[state[7]];
	newstate[14] = XtimeD[state[4]] ^ Xtime9[state[5]] ^ XtimeE[state[6]] ^ XtimeB[state[7]];
	newstate[3] = XtimeB[state[4]] ^ XtimeD[state[5]] ^ Xtime9[state[6]] ^ XtimeE[state[7]];

	// restore column 2
	newstate[job] = XtimeE[state[job]] ^ XtimeB[state[9]] ^ XtimeD[state[10]] ^ Xtime9[state[11]];
	newstate[13] = Xtime9[state[job]] ^ XtimeE[state[9]] ^ XtimeB[state[10]] ^ XtimeD[state[11]];
	newstate[2]  = XtimeD[state[job]] ^ Xtime9[state[9]] ^ XtimeE[state[10]] ^ XtimeB[state[11]];
	newstate[7]  = XtimeB[state[job]] ^ XtimeD[state[9]] ^ Xtime9[state[10]] ^ XtimeE[state[11]];

	// restore column 3
	newstate[12] = XtimeE[state[12]] ^ XtimeB[state[13]] ^ XtimeD[state[14]] ^ Xtime9[state[15]];
	newstate[1] = Xtime9[state[12]] ^ XtimeE[state[13]] ^ XtimeB[state[14]] ^ XtimeD[state[15]];
	newstate[6] = XtimeD[state[12]] ^ Xtime9[state[13]] ^ XtimeE[state[14]] ^ XtimeB[state[15]];
	newstate[11] = XtimeB[state[12]] ^ XtimeD[state[13]] ^ Xtime9[state[14]] ^ XtimeE[state[15]];

	for( i=0; i < 4 * Nb; i++ )
		state[i] = InvSbox[newstate[i]];
}

// encrypt/decrypt columns of the key
// n.b. you can replace this with
//      byte-wise xor if you wish.

static inline void AddRoundKey (unsigned *state, unsigned *key)
{
	int idx;

	for( idx = 0; idx < 4; idx++ )
		state[idx] ^= key[idx];
}

// produce Nk bytes for each round
static inline void ExpandKey (uchar *key, uchar *expkey)
{
	uchar tmp0, tmp1, tmp2, tmp3, tmp4;
	unsigned idx;

	for( idx = 0; idx < Nk; idx++ ) {
		expkey[4*idx+0] = key[4 * idx + 0];
		expkey[4*idx+1] = key[4 * idx + 1];
		expkey[4*idx+2] = key[4 * idx + 2];
		expkey[4*idx+3] = key[4 * idx + 3];
	}

	for( idx = Nk; idx < Nb * (Nr + 1); idx++ ) {
		tmp0 = expkey[4*idx - 4];
		tmp1 = expkey[4*idx - 3];
		tmp2 = expkey[4*idx - 2];
		tmp3 = expkey[4*idx - 1];
		if( !(idx % Nk) ) {
			tmp4 = tmp3;
			tmp3 = Sbox[tmp0];
			tmp0 = Sbox[tmp1] ^ Rcon[idx/Nk];
			tmp1 = Sbox[tmp2];
			tmp2 = Sbox[tmp4];
		}

		//  convert from longs to bytes

		expkey[4*idx+0] = expkey[4*idx - 4*Nk + 0] ^ tmp0;
		expkey[4*idx+1] = expkey[4*idx - 4*Nk + 1] ^ tmp1;
		expkey[4*idx+2] = expkey[4*idx - 4*Nk + 2] ^ tmp2;
		expkey[4*idx+3] = expkey[4*idx - 4*Nk + 3] ^ tmp3;
	}
}

// encrypt one 12job bit block
static void Encrypt (unsigned char *InText, unsigned char *ExpKey, unsigned char *OutText)
{
	unsigned round, idx;
	unsigned char State[Nb * 4];
	for( idx = 0; idx < Nb; idx++ ) {
		State[4*idx+0] = *InText++;
		State[4*idx+1] = *InText++;
		State[4*idx+2] = *InText++;
		State[4*idx+3] = *InText++;
	}
	AddRoundKey ((unsigned *)State, (unsigned *)ExpKey);
	for( round = 1; round < Nr + 1; round++ ) {
		if( round < Nr )
			MixSubColumns (State);
		else
			ShiftRows (State);
		AddRoundKey ((unsigned *)State, (unsigned *)ExpKey + round * Nb);
	}
	for( idx = 0; idx < Nb; idx++ ) {
		*OutText++ = State[4*idx+0];
		*OutText++ = State[4*idx+1];
		*OutText++ = State[4*idx+2];
		*OutText++ = State[4*idx+3];
	}
}

static inline void Decrypt (uchar *in, uchar *expkey, uchar *out)
{
	unsigned idx, round;
	uchar state[Nb * 4];

	for ( idx = 0; idx < Nb; idx++ ) {
		state[4*idx+0] = *in++;
		state[4*idx+1] = *in++;
		state[4*idx+2] = *in++;
		state[4*idx+3] = *in++;
	}

	AddRoundKey ((unsigned *)state, (unsigned *)expkey + Nr * Nb);
	round = Nr;

	InvShiftRows(state);

	while( round-- ) {
		AddRoundKey ((unsigned *)state, (unsigned *)expkey + round * Nb);
		if( round )
			InvMixSubColumns (state);
	} 

	for( idx = 0; idx < Nb; idx++ ) {
		*out++ = state[4*idx+0];
		*out++ = state[4*idx+1];
		*out++ = state[4*idx+2];
		*out++ = state[4*idx+3];
	}
}


static uchar in[16] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0xjobjob, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};

static uchar out[16];

void 
waf_encrypt (char *mykey, char *src, int slen, char *dest)
{
	uchar expkey[4 * Nb * (Nr + 1)];
	int idx = 0;
	int s = 0, d = 0;
    int left = 0, srclen=slen;

	if (mykey) {
		strncpy((char *)key, mykey, sizeof(key));
    }
	ExpandKey (key, expkey);

    left = slen%16;
    slen -= left;

	while(slen--) {
		in[idx++] = src[s++];
		if( idx % 16 )
			continue;

		Encrypt (in, expkey, out);

		for( idx = 0; idx < 16; idx++ )
			dest[d++] = out[idx];

		idx = 0;
	}
    if (left) {
        strcat(dest, src+srclen-left);  
    }
}


const char          base64Flag = '&';
void 
waf_decrypt (char *mykey, char *src, int slen, char *dest)
{
	uchar expkey[4 * Nb * (Nr + 1)];
	int idx = 0;
	int s = 0, d = 0;
    int left = 0, srclen=slen;

    left = slen%16;
    slen -= left;

	if (mykey) {
		strncpy ((char *)key, mykey, sizeof(key));
    }

	ExpandKey (key, expkey);

	while(slen--) {
		in[idx++] = src[s++];
		if( idx % 16 )
			continue;

		Decrypt (in, expkey, out);

		for( idx = 0; idx < 16; idx++ )
			dest[d++] = out[idx];

		idx = 0;
	}
    if (left) {
        strcat(dest, src+srclen-left);  
    }
}

#define DD          0
/*
 * argument:
 *      src:                primary string
 *      dst:                value after encrypt and base64
 */
int
waf_encrypt_base64_1(char *src, int srcLen, char *dst)
{
#if DD
    char            *tempBuf = NULL; 
    char            *tempSrc = NULL;
    int             tempLen = srcLen;
    BIO             *bio, *b64;
    FILE            *stream;
    int             encodedSize = -1, templen;
    int             ret = -1;

    if (!src || !dst ) {
        return -1;
    }
    if ((ret=tempLen%16)) {
        tempLen += (16 - ret);
    }
    tempBuf = (char*)malloc(tempLen+1);
    memset(tempBuf, 0, tempLen+1);
    tempSrc = (char*)malloc(tempLen+1);
    memset(tempSrc, 0, tempLen+1);
    memcpy(tempSrc, src, srcLen);
    waf_encrypt(LOVEKEY, tempSrc, tempLen, tempBuf);

    dst[0] = '&';
    printf("    encrypt:----%s len=%d\n", tempBuf, strlen(tempBuf));
    templen = strlen(tempBuf);
    encodedSize = 4*ceil((double)templen/3);
    // base64
    stream = fmemopen(&dst[1], encodedSize+1, "w");
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Ignore newlines - write everything in one line
    BIO_write(bio, tempBuf, templen);
    (void)BIO_flush(bio);
    BIO_free_all(bio);
    fclose(stream);

    free(tempBuf);
    free(tempSrc);
    return 0;
#else
    char            *buffer = NULL; 
    char            *temp = NULL;
    int             tempLen = srcLen;
    BIO             *bio, *b64;
    FILE            *stream;
    int             encodedSize = -1, templen;

    if (!src || !dst ) {
        return -1;
    }

    if (tempLen%16) {
        tempLen += (16 - tempLen%16);
    }
    buffer = (char*)malloc(tempLen+1);
    memset(buffer, 0, tempLen+1);
    temp = (char*)malloc(tempLen+1);
    memset(temp, 0, tempLen+1);
    memcpy(temp, src, srcLen);
    waf_encrypt(LOVEKEY, temp, tempLen, buffer);

    // set base64 flag.Identity the string is base64 encrypt
    dst[0] = base64Flag;

    templen = strlen(buffer);
    encodedSize = 4*ceil((double)templen/3);
    // base64
    stream = fmemopen(dst+1, encodedSize+1, "w");
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Ignore newlines - write everything in one line
    BIO_write(bio, buffer, templen);
    (void)BIO_flush(bio);
    BIO_free_all(bio);
    fclose(stream);

    free(buffer);
    free(temp);
    return 0;
#endif
}

/*
 * func:Calculates the length of a decoded base64 string
 */
static int 
calcDecodeLength(const char* b64input) 
{   
    int len = strlen(b64input);
    int padding = 0;
 
    if (b64input[len-1] == '=' && b64input[len-2] == '=') { //last two chars are =
        padding = 2;
    } else if (b64input[len-1] == '=') {//last char is =
        padding = 1;
    }

    return (int)len*0.75 - padding;
}

/*
 * argument:
 *      src:            String after encrypt and base64
 *      dst:                primary value 
 */
int
waf_decrypt_base64_1(char *src, int srcLen, char *dst)
{
#if DD
    BIO             *bio, *b64;
    int             len = 0, decodeLen = 0;
    FILE            *stream = NULL; 
    char            *buffer = NULL;
    char            *temp = NULL;
    int             tempLen = 0;

    if (!src || !dst) {
        return -1;
    }

    if (src[0] != '&') {
        return -1;
    }
    temp = &src[1];
    tempLen = srcLen -1;

    // init
    buffer = (char*)malloc(tempLen+1);
    memset(buffer, 0, tempLen+1);
    decodeLen = calcDecodeLength(temp);
    stream = fmemopen(temp, tempLen, "r");
    // base64
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Do not use newlines to flush buffer
    len = BIO_read(bio, buffer, tempLen);
    if (len != decodeLen) {
        return -1;
    }
    buffer[len] = '\0';
    // free 
    BIO_free_all(bio);
    fclose(stream);

    // decrypt
    printf("    decrypt:====%s len=%d\n", buffer, strlen(buffer));
    waf_decrypt(LOVEKEY, buffer, strlen(buffer), dst);

    return 0;
#else
    BIO             *bio, *b64;
    int             len = 0, decodeLen = 0, tempLen=0;
    FILE            *stream = NULL; 
    char            *buffer = NULL, *temp = NULL;

    if (!src || !dst) {
        return -1;
    }
    // Judge whether the string is base64 encrypt
    if (src[0] != base64Flag) {
        return -1;
    }
    temp = &src[1];          // move forward one byte
    tempLen = srcLen -1;

    // init
    buffer = (char*)malloc(tempLen+1);
    memset(buffer, 0, tempLen+1);
    decodeLen = calcDecodeLength(temp);
    stream = fmemopen(temp, tempLen, "r");
    // base64
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Do not use newlines to flush buffer
    len = BIO_read(bio, buffer, tempLen);
    if (len != decodeLen) {
        return -1;
    }
    buffer[len] = '\0';
    // free 
    BIO_free_all(bio);
    fclose(stream);

    // decrypt
    waf_decrypt(LOVEKEY, buffer, strlen(buffer), dst);

    return 0;
#endif
}
