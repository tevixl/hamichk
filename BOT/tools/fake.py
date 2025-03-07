import httpx
from pyrogram import Client, filters
from faker import Faker
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

locales = {
    'us': 'en_US', 'uk': 'en_GB', 'ca': 'en_CA', 'au': 'en_AU', 'de': 'de_DE',
    'fr': 'fr_FR', 'in': 'en_IN', 'jp': 'ja_JP', 'cn': 'zh_CN', 'br': 'pt_BR',
    'bd': 'bn_BD', 'pk': 'ur_PK', 'ng': 'en_NG', 'za': 'en_ZA', 'it': 'it_IT',
    'es': 'es_ES', 'ru': 'ru_RU', 'kr': 'ko_KR', 'mx': 'es_MX', 'nl': 'nl_NL',
    'pl': 'pl_PL', 'se': 'sv_SE', 'fi': 'fi_FI', 'dk': 'da_DK', 'no': 'no_NO',
    'gr': 'el_GR', 'ar': 'ar_AE', 'tr': 'tr_TR', 'id': 'id_ID', 'th': 'th_TH',
    'vn': 'vi_VN', 'ph': 'en_PH', 'my': 'ms_MY', 'sg': 'en_SG', 'ie': 'en_IE',
    'pt': 'pt_PT', 'ch': 'de_CH', 'at': 'de_AT', 'be': 'nl_BE', 'cz': 'cs_CZ',
    'hu': 'hu_HU', 'ro': 'ro_RO', 'bg': 'bg_BG', 'sk': 'sk_SK', 'si': 'sl_SI',
    'ua': 'uk_UA', 'by': 'be_BY', 'il': 'he_IL', 'sa': 'ar_SA', 'ae': 'ar_AE',
    'eg': 'ar_EG', 'ma': 'fr_MA', 'dz': 'fr_DZ', 'tn': 'fr_TN', 'gh': 'en_GH',
    'ke': 'en_KE', 'tz': 'sw_TZ', 'ug': 'en_UG', 'mm': 'my_MM', 'lk': 'si_LK',
    'np': 'ne_NP', 'kh': 'km_KH', 'la': 'lo_LA', 'bn': 'ms_BN', 'mv': 'dv_MV',
    'iq': 'ar_IQ', 'ir': 'fa_IR', 'sy': 'ar_SY', 'af': 'fa_AF', 'om': 'ar_OM',
    'ye': 'ar_YE', 'qa': 'ar_QA', 'bh': 'ar_BH', 'kw': 'ar_KW', 'jo': 'ar_JO',
    'lb': 'ar_LB', 'ps': 'ar_PS', 've': 'es_VE', 'cl': 'es_CL', 'co': 'es_CO',
    'pe': 'es_PE', 'ar': 'es_AR', 'uy': 'es_UY', 'py': 'es_PY', 'bo': 'es_BO',
    'cr': 'es_CR', 'pa': 'es_PA', 'do': 'es_DO', 'ec': 'es_EC', 'gt': 'es_GT',
    'hn': 'es_HN', 'ni': 'es_NI', 'sv': 'es_SV', 'jm': 'en_JM', 'tt': 'en_TT',
    'bb': 'en_BB', 'bs': 'en_BS', 'ht': 'fr_HT'
}


@Client.on_message(filters.command("fake", [".", "/"]))
async def cmd_fake(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]

        if len(message.text.split(" ")) > 1:
            country_code = message.text.split(" ")[1].lower()
        else:
            country_code = 'us' 

        locale = locales.get(country_code, 'en_US')

        fake = Faker(locale)

        try:
            fake_name = fake.name()
            fake_address = fake.street_address()
            fake_city = fake.city()
            fake_state = getattr(fake, 'state', lambda: 'N/A')() 
            fake_country = fake.country()
            fake_zipcode = getattr(fake, 'postcode', lambda: 'N/A')() 
            fake_gender = fake.random_element(['Male', 'Female'])
            fake_phone = fake.phone_number()

            resp = f"""
<b>Fake Info Created Successfully ✅</b>
━━━━━━━━━━━━━━
🆔 <b>Full Name:</b> <code>{fake_name}</code>
👤 <b>Gender:</b> <code>{fake_gender}</code>
🏠 <b>Street:</b> <code>{fake_address}</code>
🏙️ <b>City/Town/Village:</b> <code>{fake_city}</code>
🌍 <b>State/Province/Region:</b> <code>{fake_state}</code>
📮 <b>Postal Code:</b> <code>{fake_zipcode}</code>
📞 <b>Phone Number:</b> <code>{fake_phone}</code>
🌏 <b>Country:</b> <code>{fake_country}</code>
━━━━━━━━━━━━━━
<b>Checked By:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
<b>Bot by:</b> @tevixl
"""
            await message.reply_text(resp)  

        except Exception as e:
            import traceback
            await error_log(traceback.format_exc())

    except Exception as outer_exception:
        import traceback
        await error_log(traceback.format_exc())
