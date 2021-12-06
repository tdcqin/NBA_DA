# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 21:15
# @Author  : Ben
import random
import ssl
import requests
import re
import urllib.request
import urllib3
import pandas as pd


class NBA_crawl(object):
    def __init__(self):
        self.nba_session = requests.session()
        self.headers = {
            'User - Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        self.ip_dic = {'1': '58.218.200.223:30414',
                       '2': '58.218.200.223: 30009',
                       '3': '58.218.200.223: 30115',
                       '4': '58.218.200.223: 30020',
                       '5': '58.218.200.223: 30095',
                       '6': '58.218.200.223: 30457',
                       '7': '58.218.200.223: 30363',
                       '8': '58.218.200.223: 30116',
                       '9': '58.218.200.223: 30186',
                       '10': '58.218.200.223: 30415',
                       '11': '58.218.200.223: 30486',
                       '12': '58.218.200.223: 30259',
                       '13': '58.218.200.223: 30193',
                       '14': '58.218.200.223: 30423',
                       '15': '58.218.200.223: 30137',
                       '16': '58.218.200.223: 30059',
                       '17': '58.218.200.223: 30120',
                       '18': '58.218.200.223: 30303',
                       '19': '58.218.200.223: 30499',
                       '20': '58.218.200.223: 30352',
                       '21': '58.218.200.223: 30078',
                       '22': '58.218.200.223: 30290',
                       '23': '58.218.200.223: 30457',
                       '24': '58.218.200.223: 30281',
                       '25': '58.218.200.223: 30427',
                       '26': '58.218.200.223: 30197',
                       '27': '58.218.200.223: 30082',
                       '28': '58.218.200.223: 30461',
                       '29': '58.218.200.223: 30209',
                       '30': '58.218.200.223: 30416',
                       '31': '58.218.200.223: 30117',
                       '32': '58.218.200.223: 30470',
                       '33': '58.218.200.223: 30354',
                       '34': '58.218.200.223: 30301',
                       '35': '58.218.200.223: 30115',
                       '36': '58.218.200.223: 30071',
                       '37': '58.218.200.223: 30119',
                       '38': '58.218.200.223: 30464',
                       '39': '58.218.200.223: 30264',
                       '40': '58.218.200.223: 30027',
                       '41': '58.218.200.223: 30179'
                       }
    def player_all_request(self, player_id):  # 模块一：爬取球员所有场次数据，转化为字典
        first_url = "http://www.stat-nba.com/query.php?page=0&QueryType=game&GameType=season&Player_id=%d&crtcol=season&order=1" % player_id
        first_response = self.nba_session.get(url=first_url, headers=self.headers, timeout=6)
        first_response.encoding = 'utf-8'
        first_response = first_response.text
        total_regex = re.compile(r'<font\sclass="sstrong">共<\/font>(.*?)<font')
        total_pages = int(int(total_regex.search(first_response).group(1)) / 20)  # 计算出总页数
        # player_name_regex = re.compile(r'<font\sclass=\'sstrong\'>球员<\/font>(.*?)<\/div>')
        # player_name = player_name_regex.search(first_response).group(1)  # 爬取球员姓名
        number_list = []
        board_list = []
        assist_list = []
        score_list = []
        for i in range(0, total_pages + 1):
            url = "http://www.stat-nba.com/query.php?page=%d&QueryType=game&GameType=season&Player_id=1862&crtcol=season&order=1" % i
            response = self.nba_session.get(url=url, headers=self.headers, timeout=6)
            response.encoding = 'utf-8'
            response = response.text;
            # print(response)
            number_regex = re.compile(r'<td\sclass="normal\srow\schange_color\scol0\srow\d+">(\d+)</td>')
            number_list += (number_regex.findall(response))
            # 爬取篮板数
            board_regex = re.compile(r'<td\sclass="normal\strb change_color\scol16\srow\d+">(\d+)</td>')
            board_list += board_regex.findall(response)
            # 爬取助攻数
            assist_regex = re.compile(r'<td\sclass="normal\sast\schange_color\scol19\srow\d+">(\d+)</td>')
            assist_list += assist_regex.findall(response)
            # print(assist)
            # 爬取得分数
            score_regex = re.compile(r'<td\sclass="normal\spts\schange_color\scol24\srow\d+">(\d+)</td>')
            score_list += score_regex.findall(response)
        career_dic = {
            'ids': number_list,
            'boards': board_list,
            'assists': assist_list,
            'scores': score_list
        }
        return career_dic

    def season_all_request(self, start, end):  # 模块二：爬取指定赛季的数据
        season_start_end_dic = {}
        first_url = "http://www.stat-nba.com/query.php?QueryType=ss&SsType=season&AT=avg&order=1&crtcol=pts&PageNum=20&Season0=%s&Season1=%s" % (
            start, end)
        first_response = self.nba_session.get(url=first_url, headers=self.headers, timeout=6)
        first_response.encoding = 'utf-8'
        first_response = first_response.text
        total_regex = re.compile(r'<font\sclass="sstrong">共<\/font>(.*?)<font')
        total_pages = int(int(total_regex.search(first_response).group(1)) / 20)  # 计算出总页数
        data = [
            {'value': 0, 'name': '10以下'},
            {'value': 0, 'name': '10-15'},
            {'value': 0, 'name': '15-20'},
            {'value': 0, 'name': '20-25'},
            {'value': 0, 'name': '25-30'},
            {'value': 0, 'name': '30以上'}
        ]
        for i in range(0, total_pages + 1):
            url = "http://www.stat-nba.com/query.php?page=%d&QueryType=ss&SsType=season&AT=avg&order=1&crtcol=pts&PageNum=20&Season0=%s&Season1=%s#label_show_result" % (
                i, start, end)
            response = self.nba_session.get(url=url, headers=self.headers, timeout=6)
            response.encoding = 'utf-8'
            response = response.text;
            for i in range(0, 20):
                try:
                    # 爬取球员ID和姓名
                    player_id_name_regex = re.compile(
                        r'<td\sclass="normal\splayer_name_out\schange_color\scol1\srow(%d)"><a\sclass=\'query_player_name\'\shref=\'./player/(\d+).html\'\starget=\'_blank\'>(.*?)</a></td>' % i)
                    player_id = player_id_name_regex.search(response).group(2)
                    player_name = player_id_name_regex.search(response).group(3)
                    # 爬取得分数
                    score_regex = re.compile(r'<td\sclass="current\spts\schange_color\scol24\srow(%d)">(.*?)</td>' % i)
                    score = float(score_regex.search(response).group(2))
                    # print(f"{player_id}:{player_name}的场均：{score}")
                    if score < 10.0:
                        data[0]['value'] += 1
                    elif 10.0 <= score < 15.0:
                        data[1]['value'] += 1
                        # data[1].update({'value': data[1].get('value') + 1, 'name': '10-15'})
                    elif 15.0 <= score < 20.0:
                        data[2]['value'] += 1
                    elif 20.0 <= score < 25.0:
                        data[3]['value'] += 1
                    elif 25.0 <= score < 30.0:
                        data[4]['value'] += 1
                    else:
                        data[5]['value'] += 1
                    # season_2018_2019_dao.insertItem(player_id, player_name, score)
                except:
                    season_start_end_dic = {
                        'data': data
                    }
        return season_start_end_dic

    def salary_request(self, player_id):  # 模块四：爬取id指定球员薪资情况
        # 格式：{'years':[2013-14,2015-06]，'salarys':[2000,3000,4000]}
        first_url = "http://www.stat-nba.com/player/%d.html" % player_id
        first_response = self.nba_session.get(url=first_url, headers=self.headers, timeout=6)
        first_response.encoding = 'utf-8'
        first_response = first_response.text
        year_regex = re.compile(r'<td\sclass="current">(.*?)</td>')
        year_list = year_regex.findall(first_response)
        salary_regex = re.compile(
            r'<td\sclass="current">.*?</td>[\s\S]*?<td\sclass="normal"\sstyle="font-weight:\s\sbold">(\d+)万美元</td>')
        salary_list = salary_regex.findall(first_response)
        salary_dic = {
            'years': year_list,
            'salary': salary_list
        }
        return salary_dic

    def player_detail_information(self, player_id):
        urllib.request.urlretrieve('http://www.stat-nba.com/image/playerImage/%s.jpg' % player_id,
                                   '.\static\player_images\%s.jpg' % player_id)
        first_url = "http://www.stat-nba.com/player/%d.html" % player_id
        first_response = self.nba_session.get(url=first_url, headers=self.headers, timeout=6)
        first_response.encoding = 'utf-8'
        first_response = first_response.text
        key_regex = re.compile(r'<div class="column">(.*?):</div>')
        key_list = key_regex.findall(first_response)
        value_regex = re.compile(r'<div class="column">.*</div>(.*?)<')
        value_list = value_regex.findall(first_response)
        draft_regex = re.compile(r'<div class="column">.*</div>([^<]*?)<a href="\.\./team/')
        draft = draft_regex.findall(first_response)
        draft_regex_2 = re.compile(r'<a href="../team/.*.html" target="_blank">(.*?)</a>')
        draft_2 = draft_regex_2.findall(first_response)
        draft_imformation = draft[0].strip() + draft_2[0] + '选中'
        value_list.insert(len(key_list) - 2, draft_imformation)
        dict_ = dict()
        for i in range(len(key_list)):
            temp = {key_list[i]: value_list[i]}
            dict_.update(temp)
        return dict_

    def name_id_search(self, name):  # 模糊搜索，爬取匹配到的球员中文名，英文名和id
        name_id_dic = {}
        url = "http://www.stat-nba.com/playerList.php?name=%s" % name  # 把name换掉就行
        response = self.nba_session.get(url=url, headers=self.headers, timeout=6)
        response.encoding = 'utf-8'
        response = response.text
        name_id_regex = re.compile(
            r'<a\sclass=".*?"\shref="./player/(\d+).html"\sid="cover\d+"\shidefocus="true"\starget="_blank">\n<span>\n(.*?)/(.*?)\n</span>')
        name_id = name_id_regex.findall(response)
        # 返回格式：{'詹姆斯':[英文名字,中文id]}
        for i in range(0, len(name_id)):
            player_name_ch = name_id[i][1]
            player_name_en = name_id[i][2]
            player_id = name_id[i][0]
            name_id_temp_dic = {
                player_name_ch: [player_name_en, player_id]
            }
            name_id_dic.update(name_id_temp_dic)
        return name_id_dic

    def get_en_player_id(self, name):

        dict_ = {'James Harden': '201935', 'Paul George': '202331', 'Giannis Antetokounmpo': '203507',
                 'Joel Embiid': '203954', 'Stephen Curry': '201939', 'Kawhi Leonard': '202695',
                 'Devin Booker': '1626164', 'Kevin Durant': '201142', 'Damian Lillard': '203081',
                 'Kemba Walker': '202689', 'Bradley Beal': '203078', 'Blake Griffin': '201933',
                 'Karl-Anthony Towns': '1626157', 'Kyrie Irving': '202681', 'Donovan Mitchell': '1628378',
                 'Zach LaVine': '203897', 'Russell Westbrook': '201566', 'Klay Thompson': '202691',
                 'Julius Randle': '203944', 'LaMarcus Aldridge': '200746', 'DeMar DeRozan': '201942',
                 'Luka Doncic': '1629029', 'Jrue Holiday': '201950', "D'Angelo Russell": '1626156',
                 'Mike Conley': '201144', 'CJ McCollum': '203468', 'Nikola Vucevic': '202696', 'Buddy Hield': '1627741',
                 'Nikola Jokic': '203999', 'Tobias Harris': '202699', 'Lou Williams': '101150',
                 'Danilo Gallinari': '201568', 'John Collins': '1628381', 'Trae Young': '1629027',
                 'Jimmy Butler': '202710', 'Kyle Kuzma': '1628398', 'Khris Middleton': '203114',
                 'Jamal Murray': '1627750', 'Andrew Wiggins': '203952', 'Tim Hardaway Jr.': '203501',
                 'JJ Redick': '200755', 'Bojan Bogdanovic': '202711', 'Andre Drummond': '203083',
                 "De'Aaron Fox": '1628368', 'Pascal Siakam': '1627783', 'Ben Simmons': '1627732',
                 'Jordan Clarkson': '203903', 'Spencer Dinwiddie': '203915', 'Collin Sexton': '1629012',
                 'Clint Capela': '203991', 'Montrezl Harrell': '1626149', 'Josh Richardson': '1626196',
                 'Harrison Barnes': '203084', 'Deandre Ayton': '1629028', 'Eric Gordon': '201569',
                 'Aaron Gordon': '203932', 'Eric Bledsoe': '202339', 'Rudy Gobert': '203497', 'Jayson Tatum': '1628369',
                 'Malcolm Brogdon': '1627763', 'Jusuf Nurkic': '203994', 'Chris Paul': '101108',
                 'Dennis Schroder': '203471', 'Reggie Jackson': '202704', 'Jeremy Lamb': '203087',
                 'Kelly Oubre Jr.': '1626162', 'Evan Fournier': '203095', 'Terrence Ross': '203082',
                 'Dwyane Wade': '2548', 'Serge Ibaka': '201586', 'Marvin Bagley III': '1628963',
                 'Emmanuel Mudiay': '1626144', 'Jabari Parker': '203953', 'Kyle Lowry': '200768',
                 'Bogdan Bogdanovic': '203992', 'Domantas Sabonis': '1627734', 'Marcus Morris': '202694',
                 'Steven Adams': '203500', 'Jaren Jackson Jr.': '1628991', 'Rudy Gay': '200752', 'Joe Harris': '203925',
                 'Enes Kanter': '202683', 'Jerami Grant': '203924', 'Al Horford': '201143', 'Marc Gasol': '201188',
                 'Myles Turner': '1626167', 'Cedi Osman': '1626224', 'Jaylen Brown': '1627759', 'Kevin Knox': '1628995',
                 'Ricky Rubio': '201937', 'Thaddeus Young': '201152', 'Paul Millsap': '200794',
                 'Justise Winslow': '1626159', 'Trevor Ariza': '2772', 'Brook Lopez': '201572',
                 'Hassan Whiteside': '202355', 'Jeff Green': '201145', 'Wesley Matthews': '202083',
                 'Joe Ingles': '204060', 'JaVale McGee': '201580', 'Willie Cauley-Stein': '1626161',
                 'Jae Crowder': '203109', 'Derrick Favors': '202324', 'Bryn Forbes': '1627854',
                 'D.J. Augustin': '201571', 'Kent Bazemore': '203145', 'Josh Jackson': '1628367',
                 'Gordon Hayward': '202330', 'Kentavious Caldwell-Pope': '203484', 'Malik Beasley': '1627736',
                 'Reggie Bullock': '203493', 'Darren Collison': '201954', 'Rodney Hood': '203918',
                 'DeMarre Carroll': '201960', 'Alex Len': '203458', 'DeAndre Jordan': '201599',
                 'Fred VanVleet': '1627832', 'Jarrett Allen': '1628386', 'Trey Burke': '203504',
                 'Allonzo Trier': '1629019', 'Shai Gilgeous-Alexander': '1628983', 'Dewayne Dedmon': '203473',
                 'Taj Gibson': '201959', 'Damyean Dotson': '1628422', 'Dario Saric': '203967',
                 'Dwight Powell': '203939', 'Thomas Bryant': '1628418', 'Marco Belinelli': '201158',
                 'Justin Holiday': '203200', 'Monte Morris': '1628420', 'Danny Green': '201980',
                 'Tyreke Evans': '201936', 'Marvin Williams': '101107', 'Kelly Olynyk': '203482',
                 'Avery Bradley': '202340', 'Derrick White': '1628401', 'Patty Mills': '201988',
                 'Luke Kennard': '1628379', 'Kevin Huerter': '1628989', 'Nemanja Bjelica': '202357',
                 'Jonathan Isaac': '1628371', 'Jeremy Lin': '202391', 'Robin Lopez': '201577',
                 'Markieff Morris': '202693', 'JaMychal Green': '203210', 'Al-Farouq Aminu': '202329',
                 'Larry Nance Jr.': '1626204', 'Nicolas Batum': '201587', 'Jalen Brunson': '1628973',
                 'Gerald Green': '101123', 'Landry Shamet': '1629013', 'Terry Rozier': '1626179',
                 'Malik Monk': '1628370', 'Rondae Hollis-Jefferson': '1626178', 'Ivica Zubac': '1627826',
                 'Bam Adebayo': '1628389', 'Tomas Satoransky': '203107', 'Marcus Smart': '203935',
                 'Mario Hezonja': '1626209', 'Alec Burks': '202692', 'Delon Wright': '1626153',
                 'Norman Powell': '1626181', 'Kyle Korver': '2594', 'Trey Lyles': '1626168',
                 'Rodions Kurucs': '1629066', 'Langston Galloway': '204038', 'Noah Vonleh': '203943',
                 "DeAndre' Bembry": '1627761', 'Mikal Bridges': '1628969', 'Darius Miller': '203121',
                 'Jahlil Okafor': '1626143', 'Richaun Holmes': '1626158', 'Austin Rivers': '203085',
                 'Frank Jackson': '1628402', 'Davis Bertans': '202722', 'Jamal Crawford': '2037',
                 'Seth Curry': '203552', 'Josh Hart': '1628404', 'Garrett Temple': '202066', 'Ante Zizic': '1627790',
                 'Mason Plumlee': '203486', 'Josh Okogie': '1629006', 'Maurice Harkless': '203090',
                 'Patrick Beverley': '201976', 'George Hill': '201588', 'Rodney McGruder': '203585',
                 'Jake Layman': '1627774', 'Dorian Finney-Smith': '1627827', 'Iman Shumpert': '202697',
                 'Miles Bridges': '1628970', 'Vince Carter': '1713', 'Draymond Green': '203110',
                 'Mitchell Robinson': '1629011', 'PJ Tucker': '200782', 'Doug McDermott': '203926',
                 'Boban Marjanovic': '1626246', 'Willy Hernangomez': '1626195', 'Lance Stephenson': '202362',
                 'Justin Jackson': '1628382', 'Harry Giles III': '1628385', 'Derrick Jones Jr.': '1627884',
                 'Mike Muscala': '203488', 'OG Anunoby': '1628384', 'Terrance Ferguson': '1628390',
                 'Pat Connaughton': '1626192', 'Tyus Jones': '1626145', 'Stanley Johnson': '1626169',
                 'Quinn Cook': '1626188', 'Wayne Selden': '1627782', 'Maxi Kleber': '1628467', 'Evan Turner': '202323',
                 'Ersan Ilyasova': '101141', 'Ryan Arcidiacono': '1627853', 'James Ennis III': '203516',
                 'Ian Clark': '203546', 'Michael Kidd-Gilchrist': '203077', 'Zach Collins': '1628380',
                 'Cory Joseph': '202709', 'Shaquille Harrison': '1627885', 'Sterling Brown': '1628425',
                 'Gorgui Dieng': '203476', 'T.J. McConnell': '204456', 'Devin Harris': '2734',
                 'Jonas Jerebko': '201973', 'Kevon Looney': '1626172', 'Cheick Diallo': '1627767',
                 'Tony Snell': '203503', 'Yogi Ferrell': '1627812', 'Nik Stauskas': '203917',
                 'Meyers Leonard': '203086', 'Juancho Hernangomez': '1627823', 'Ed Davis': '202334',
                 'Mike Scott': '203118', 'Torrey Craig': '1628470', 'Andre Iguodala': '2738', 'Daniel Theis': '1628464',
                 'Jakob Poeltl': '1627751', 'Tim Frazier': '204025', "Royce O'Neale": '1626220',
                 'Thon Maker': '1627748', 'Anthony Tolliver': '201229', 'Wes Iwundu': '1628411',
                 'Nerlens Noel': '203457', 'Jared Dudley': '201162', 'Alfonzo McKinnie': '1628035',
                 'Bruce Brown': '1628971', 'Jerian Grant': '1626170', 'Shaun Livingston': '2733',
                 'Cristiano Felicio': '1626245', 'Georges Niang': '1627777', 'Abdel Nader': '1627846',
                 'Zaza Pachulia': '2585', 'TJ Leaf': '1628388', 'Patrick Patterson': '202335',
                 'Tyrone Wallace': '1627820', 'Jordan Bell': '1628395', 'Dante Cunningham': '201967',
                 'Sindarius Thornwell': '1628414', 'LeBron James': '2544'}
        return dict_[name]

    def x_y_made_request(self, player_ch_id, player_en_name):  # 爬取X，Y，和是否投进0，1 绘制热点图的数据
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib3.disable_warnings()
        i = str(random.randint(1, len(self.ip_dic)))
        ip = self.ip_dic.get(i)
        # proxyinfo = "http://%s:%s@%s:%s" % ('阿布云证书', '阿布云密钥', 'http-dyn.abuyun.com', '9020')
        # proxyinfo = '36.6.224.251:4262'
        # proxy = {
        #     "http": proxyinfo,
        #     "https": proxyinfo
        # }
        season_list = self.salary_request(int(player_ch_id)).get('years')
        for i in range(0, len(season_list)):
            season_list[i] = str(20) + season_list[i]
        player_en_id = self.get_en_player_id(player_en_name)
        x_y_made_dic = {}
        list_made = list()
        list_nomade = list()
        for i in range(0, len(season_list)):
            season = season_list[i]
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib3.disable_warnings()
            url = "https://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=%s&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=%s&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=%s&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0&PlayerPosition=" % (
                season, player_en_id, season)
            headers = {'User-Agent': 'chrome'}
            # 请求含有球员投球数据的url
            response = self.nba_session.get(url, headers=headers, timeout=60,verify=False)
            data = response.json()
            # 获取列名即每项投球数据的意思
            headers = data['resultSets'][0]['headers']
            # 获取投球的相关数据
            shots = data['resultSets'][0]['rowSet']
            shot_df = pd.DataFrame(shots, columns=headers)
            shot_df = shot_df[['LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG']].values.tolist()#[[],[],[]]
            for i in shot_df:
                if i[2]==1:
                    list_made.append([i[0],i[1]])
                else:
                    list_nomade.append([i[0],i[1]])
        x_y_made_dic = {
            'made': list_made,
            'no_made': list_nomade
        }
        return x_y_made_dic
nba_crwa = NBA_crawl()
