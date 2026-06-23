import re
from data import SightInfo, StationInfo, PartInfo, LineInfo

class Dini33Parser:
    def __init__(self,line_parts_list):
        self.raw_lines=line_parts_list
        self.line_info=LineInfo()
        self.line_info.LineName = "Unknown"

    def parse(self):
        """主解析入口，返回 LineInfo 对象"""
        idx=0
        total_lines=len(self.raw_lines)
        while idx < total_lines:
            parts = self.raw_lines[idx]
            if not parts or len(parts) < 3:
                idx += 1
                continue
            # 检查是否为测段开始行 (包含 "Start-Line")
            if "Start-Line" in parts[2]:
                # 开始解析一个新测段
                part, idx = self._parse_part(idx)
                if part and part.StationList:
                    self.line_info.PartList.append(part)
            else:
                idx += 1
        return self.line_info

    def _parse_part(self,start_idx):
        """从 start_idx 开始解析一个完整的测段，返回 (PartInfo, 结束索引)"""
        part=PartInfo()
        current_station=None
        station_sights=[]
        start_parts = self.raw_lines[start_idx]
        match_num=re.search(r'aBFFB\s+(\d+)',start_parts[2])
        if match_num:
            part.partNum = int(match_num.group(1))

        idx=start_idx+1
        total=len(self.raw_lines)
        station_counter = 0

        while idx<total:
            parts=self.raw_lines[idx]
            if not parts or len(parts) < 3:
                idx += 1
                continue


            field3=parts[2].strip()
            field4 = parts[3].strip() if len(parts) > 3 else ""
            field5 = parts[4].strip() if len(parts) > 4 else ""
            field6 = parts[5].strip() if len(parts) > 5 else ""

            # 检测测段结束行 (End-Line 或 下一行有 Cont-Line 但临时中断暂时不管)
            if "End-Line" in field3:
                if station_sights:
                    self._flush_station(part, station_sights, station_counter)
                    station_counter += 1
                    station_sights = []

                # 可能 End-Line 行之后还有 Cont-Line（临时中断），但测段结束，跳出
                idx += 1
                break

            #忽略无效行
            if "#####" in field3 or "Reading E" in field4 or "Reading E" in field5:
                # 这些行应被忽略，不参与测站构建
                idx += 1
                continue

            # 提取测量读数行（包含 Rb 或 Rf）
            if "Rb" in field4 or "Rf" in field4:
                sight=self._parse_sight(parts)
                if sight:
                    station_sights.append(sight)
                    #判断是否收齐一个测站（4次观测）
                    if len(station_sights)==4:
                        self._flush_station(part, station_sights, station_counter)
                        station_counter += 1
                        station_sights = []
            elif "Sh" in field4 or "dz" in field4 or "Db" in field4:
                # 提取汇总数据，可以直接赋值给 part，便于后续验证
                self._parse_part_summary(part, field4, field5, field6)

            idx+=1
            if station_sights:
                self._flush_station(part, station_sights, station_counter)

            # 对测段执行 Reset（需要预先知道起点高程，此处先不设置 StartPtH，由外部给定）
            # 但 Reset 需要第一个测站的后视点高程，外部会在调用前设置 part.StartPtH 并手动 Reset
            # 为避免错误，这里不自动调用 Reset
            return part, idx



    def _parse_sight(self,parts,line_num):
        """从一行 parts 中提取 SightInfo，返回 SightInfo 或 None"""
        field3=parts[2].strip()
        field4=parts[3].strip()
        field5=parts[4].strip()

        if 'Rb' in field4:
            s_type="B"
        elif "Rf" in field4:
            s_type="F"
        else:
            return None

        '''提取读数'''
        rd_match=re.search(r'(\d+\.\d+)\s*m',field4)
        if not rd_match:
            return None
        rd=float(rd_match.group(1))

        '''提取视距'''
        hd=0.0
        if "HD" in field5:
            hd_match = re.search(r'(\d+\.\d+)\s*m', field5)
            if hd_match:
                hd = float(hd_match.group(1))

        '''提取点名和时间'''
        parts3=field3.split()
        pt_name=""
        time_str=""
        if len(parts3) >= 2:
            pt_name=f"{parts3[0]} {parts3[1]}"  #KD1 X1
            if len(parts3) >=3:
                time_str=parts3[2]

        adr=0
        if len(parts)>1:
            adr_match=re.search(r'\d+',parts[1])
            if adr_match:
                if adr_match:
                    adr=int(adr_match.group())

        return SightInfo(
            line_id=line_num,
            pt_name=pt_name,
            rd=rd,
            hd=hd,
            adr=adr,
            time_str=time_str,
            s_type=s_type
        )

    def _flush_station(self,part,sight_list,station_idx):
        if not sight_list:
            return
        station=StationInfo()
        station.SightList = sight_list
        part.StationList.append(station)

    def _parse_part_summary(self,part,field4,field5, field6):
        full_text = field4 + " " + field5 + " " + field6
        sh_match = re.search(r'Sh\s+(-?\d+\.\d+)\s*m', full_text)
        if sh_match:
            part.sh = float(sh_match.group(1))
        dz_match = re.search(r'dz\s+(-?\d+\.\d+)\s*m', full_text)
        if dz_match:
            part.dz = float(dz_match.group(1))
        db_match = re.search(r'Db\s+(\d+\.\d+)\s*m', full_text)
        if db_match:
            part.Db = float(db_match.group(1))
        df_match = re.search(r'Df\s+(\d+\.\d+)\s*m', full_text)
        if df_match:
            part.Df = float(df_match.group(1))