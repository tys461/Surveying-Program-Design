import math


class Point:
    def __init__(self, n, t, x, y, h, d):
        self.n = n
        self.t = t
        self.x = x
        self.y = y
        self.h = h
        self.d = d


def pshi_count(avg1, avg2, fai1, fa2, E):
    return avg1 + (avg2 - avg1) * ((abs(E) - fai1) / (fa2 - fai1))


def pgan_count(avg1, avg2, amp1, amp2, fai1, fa2, E, T):
    return ((avg1 + (avg2 - avg1) * ((abs(E) - fai1) / (fa2 - fai1))) + (amp1 +
                                                                         (amp2 - amp1) * ((abs(E) - fai1) / (
                        fa2 - fai1)) * math.cos(2 * math.pi * ((T - 28) / 365.25))))


def mapping(E_rad, a, b, c):
    sinE = math.sin(E_rad)
    num = 1 + a / (1 + b / (1 + c))
    den = sinE + a / (sinE + b / (sinE + c))
    return num / den


class PointCllection:
    def __init__(self):
        self.lis_point: list[Point] = []

        self.p_15 = {'a_avg': 0.00058021897, 'b_avg': 0.0014275268, 'c_avg': 0.043472961}
        self.p_30 = {'a_avg': 0.00056794847, 'b_avg': 0.0015138625, 'c_avg': 0.046729510}
        self.p_45 = {'a_avg': 0.00058118019, 'b_avg': 0.0014572752, 'c_avg': 0.043908931}
        self.p_60 = {'a_avg': 0.00059727542, 'b_avg': 0.0015007428, 'c_avg': 0.044626982}
        self.p_75 = {'a_avg': 0.00061641693, 'b_avg': 0.0017599082, 'c_avg': 0.054736038}

        self.pgan_15 = {'a_avg': 0.0012769934, 'b_avg': 0.0029153695, 'c_avg': 0.062610505}
        self.pgan_30 = {'a_avg': 0.0012683230, 'b_avg': 0.0029152299, 'c_avg': 0.062837393}
        self.pgan_45 = {'a_avg': 0.0012465397, 'b_avg': 0.0029288445, 'c_avg': 0.063721774}
        self.pgan_60 = {'a_avg': 0.0012196049, 'b_avg': 0.0029022565, 'c_avg': 0.063824265}
        self.pgan_75 = {'a_avg': 0.0012045996, 'b_avg': 0.0029024912, 'c_avg': 0.064258455}

        self.amp_15 = {'a_amp': 0.0, 'b_amp': 0.0, 'c_amp': 0.0}
        self.amp_30 = {'a_amp': 0.000012709626, 'b_amp': 0.000021414979, 'c_amp': 0.000090128400}
        self.amp_45 = {'a_amp': 0.000026523662, 'b_amp': 0.000030160779, 'c_amp': 0.000043497037}
        self.amp_60 = {'a_amp': 0.000034000452, 'b_amp': 0.000072562722, 'c_amp': 0.00084795348}
        self.amp_75 = {'a_amp': 0.000041202191, 'b_amp': 0.00011723375, 'c_amp': 0.0017037206}

    def shia_b_c_count(self, E):
        a_avg, b_avg, c_avg = 0, 0, 0

        if abs(E) < 15:
            a_avg = self.p_15.get('a_avg')
            b_avg = self.p_15.get('b_avg')
            c_avg = self.p_15.get('c_avg')

        if 15 < abs(E) < 30:
            a_avg = pshi_count(self.p_15.get('a_avg'), self.p_30.get('a_avg'), 15, 30, abs(E))
            b_avg = pshi_count(self.p_15.get('b_avg'), self.p_30.get('b_avg'), 15, 30, abs(E))
            c_avg = pshi_count(self.p_15.get('c_avg'), self.p_30.get('c_avg'), 15, 30, abs(E))

        if 30 < abs(E) < 45:
            a_avg = pshi_count(self.p_30.get('a_avg'), self.p_45.get('a_avg'), 30, 45, abs(E))
            b_avg = pshi_count(self.p_30.get('b_avg'), self.p_45.get('b_avg'), 30, 45, abs(E))
            c_avg = pshi_count(self.p_30.get('c_avg'), self.p_45.get('c_avg'), 30, 45, abs(E))

        if 45 < abs(E) < 60:
            a_avg = pshi_count(self.p_45.get('a_avg'), self.p_60.get('a_avg'), 45, 60, abs(E))
            b_avg = pshi_count(self.p_45.get('b_avg'), self.p_60.get('b_avg'), 45, 60, abs(E))
            c_avg = pshi_count(self.p_45.get('c_avg'), self.p_60.get('c_avg'), 45, 60, abs(E))

        if 60 < abs(E) < 75:
            a_avg = pshi_count(self.p_60.get('a_avg'), self.p_75.get('a_avg'), 60, 75, abs(E))
            b_avg = pshi_count(self.p_60.get('b_avg'), self.p_75.get('b_avg'), 60, 75, abs(E))
            c_avg = pshi_count(self.p_60.get('c_avg'), self.p_75.get('c_avg'), 60, 75, abs(E))

        if abs(E) > 75:
            a_avg = self.p_75.get('a_avg')
            b_avg = self.p_75.get('b_avg')
            c_avg = self.p_75.get('c_avg')

        return a_avg, b_avg, c_avg

    def gana_b_c_count(self, E, T):
        a_avg, b_avg, c_avg = 0, 0, 0

        if abs(E) < 15:
            a_avg = self.pgan_15.get('a_avg') + self.pgan_15.get('a_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))
            b_avg = self.pgan_15.get('b_avg') + self.pgan_15.get('b_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))
            c_avg = self.pgan_15.get('c_avg') + self.pgan_15.get('c_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))

        if 15 < abs(E) < 30:
            a_avg = pgan_count(self.pgan_15.get('a_avg'), self.pgan_30.get('a_avg'), self.amp_15.get('a_amp'),
                               self.amp_30.get('a_amp'), 15, 30, abs(E), T)
            b_avg = pgan_count(self.pgan_15.get('b_avg'), self.pgan_30.get('b_avg'), self.amp_15.get('b_amp'),
                               self.amp_30.get('b_amp'), 15, 30, abs(E), T)
            c_avg = pgan_count(self.pgan_15.get('c_avg'), self.pgan_30.get('c_avg'), self.amp_15.get('c_amp'),
                               self.amp_30.get('c_amp'), 15, 30, abs(E), T)

        if 30 < abs(E) < 45:
            a_avg = pgan_count(self.pgan_30.get('a_avg'), self.pgan_45.get('a_avg'), self.amp_30.get('a_amp'),
                               self.amp_45.get('a_amp'), 30, 45, abs(E), T)
            b_avg = pgan_count(self.pgan_30.get('b_avg'), self.pgan_45.get('b_avg'), self.amp_30.get('b_amp'),
                               self.amp_45.get('b_amp'), 30, 45, abs(E), T)
            c_avg = pgan_count(self.pgan_30.get('c_avg'), self.pgan_45.get('c_avg'), self.amp_30.get('c_amp'),
                               self.amp_45.get('c_amp'), 30, 45, abs(E), T)

        if 45 < abs(E) < 60:
            a_avg = pgan_count(self.pgan_45.get('a_avg'), self.pgan_60.get('a_avg'), self.amp_45.get('a_amp'),
                               self.amp_60.get('a_amp'), 45, 60, abs(E), T)
            b_avg = pgan_count(self.pgan_45.get('b_avg'), self.pgan_60.get('b_avg'), self.amp_45.get('b_amp'),
                               self.amp_60.get('b_amp'), 45, 60, abs(E), T)
            c_avg = pgan_count(self.pgan_45.get('c_avg'), self.pgan_60.get('c_avg'), self.amp_45.get('c_amp'),
                               self.amp_60.get('c_amp'), 45, 60, abs(E), T)

        if 60 < abs(E) < 75:
            a_avg = pgan_count(self.pgan_60.get('a_avg'), self.pgan_75.get('a_avg'), self.amp_60.get('a_amp'),
                               self.amp_75.get('a_amp'), 60, 75, abs(E), T)
            b_avg = pgan_count(self.pgan_60.get('b_avg'), self.pgan_75.get('b_avg'), self.amp_60.get('b_amp'),
                               self.amp_75.get('b_amp'), 60, 75, abs(E), T)
            c_avg = pgan_count(self.pgan_60.get('c_avg'), self.pgan_75.get('c_avg'), self.amp_60.get('c_amp'),
                               self.amp_75.get('c_amp'), 60, 75, abs(E), T)

        if abs(E) > 75:
            a_avg = self.pgan_75.get('a_avg') + self.pgan_75.get('a_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))
            b_avg = self.pgan_75.get('b_avg') + self.pgan_75.get('b_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))
            c_avg = self.pgan_75.get('c_avg') + self.pgan_75.get('c_avg') * math.cos(2 * math.pi * ((T - 28) / 365.25))

        return a_avg, b_avg, c_avg

    def mwE_count(self, E):
        red_E = math.radians(abs(E))
        sin_E = math.sin(red_E)
        a_avg, b_avg, c_avg = self.shia_b_c_count(E)
        numerator = 1 + a_avg / (1 + b_avg / (1 + c_avg))
        denominator = sin_E + a_avg / (sin_E + b_avg / (sin_E + c_avg))
        return numerator / denominator

    def mdE_count(self, E, T, H):
        red_E = math.radians(abs(E))
        sin_E = math.sin(red_E)
        a_ht = 2053e-5
        b_ht = 5.49e-3
        c_ht = 1.14e-3
        ad, bd, cd = self.gana_b_c_count(E, T)
        sinE = math.sin(red_E)
        M_base = mapping(red_E, ad, bd, cd)
        M_ht = mapping(red_E, a_ht, b_ht, c_ht)
        return M_base + (1.0 / sinE - M_ht) * (H / 1000.0)

    def s_count(self, mwE, mdE, H):
        ZHD = 2.29951 * math.pow(math.e, -0.000116 * H)
        ZWD = 0.1
        S = ZHD * mdE + mwE * ZWD
        return S, ZHD, ZWD

    def count(self):
        result = []
        for i in self.lis_point:
            T = int((i.t)[0:4]) * int((i.t)[6:8])
            n = i.n
            lat = i.x
            lng = i.y
            H = i.h
            E = i.d
            mwE = self.mwE_count(E)
            mdE = self.mdE_count(E, T, H)
            S, ZHD, ZWD = self.s_count(mwE, mdE, H)

            a = f"{n:<10} {E:>8.2f} {ZHD:>12.5f} {mdE:>12.5f} {ZWD:>10.5f} {mwE:>12.5f} {S:>14.5f}"
            result.append(a)

        return result
