from math import *
'''Функция для суммы скобки с умножением из двух массивов'''
def summmnoj(mass1, mass2):
    if len(mass1) != len(mass2):
        return 0
    else:
        summ = 0
        for i in range(len(mass1)):
            summ += mass1[i]*mass2[i]
        return summ
"""Теорема пифагора"""
def pif(ch1, ch2):
    return sqrt(ch1**2 + ch2**2)
def summ(mass1):
    n = 0
    for i in range(len(mass1)):
        n += mass1[i]
    return n

"""Интерфейс данных"""
'''gruzx, gruzy, gruzz, gruzmass - массивы в которых данные о всех грузах, формат длинна-ширина-высота-масса
vagon - массив с данными вагона формата длинна-ширина-высота-масса-длинна_базы-ширина_базы
количество груза беру из len(gruzx)
Ввод данных от 1 до последнего, если груз неустойчив то меняйте порядок
'''

vagon = [13300, 2890, 1310, float(21), 13200, 2870, 9720]
def modcalc(gruzx, gruzy, gruzz, gruzmass, vagon):
    
    '''подсчёт центра тяжести груза'''
    ctgruzx = []
    ctgruzy = []
    ctgruzz = []
    
    for i in range(len(gruzx)):
        ctgruzx.append(gruzx[i]/2)
        ctgruzy.append(gruzy[i]/2)
        ctgruzz.append(gruzz[i]/2)
    
    '''количество брусков и добавочный размер в мм'''
    bruskov = len(gruzx) + 1
    lenbruskov = bruskov * 150
    
    """координата центра тяжести груза с торца"""
    coorctgruzx = [gruzx[0]+150]#150 это брусок
    
    for i in range(1, len(gruzx)):
        coorctgruzx.append((coorctgruzx[i-1] + ctgruzx[i-1] + 150 + ctgruzx[i]))
    
    """координата центра тяжести вагона"""
    coorctvagonx = vagon[0]/2
    coorctvagonz = vagon[2]/2
#    print(ctgruzx, ctgruzy, ctgruzz, coorctgruzx)
    
    '''наветренная сторона'''
    vetst = []
    for i in range(len(gruzx)):
        vetst.append((gruzz[i]*gruzy[i])/(1000*1000))



    '''вери олд код'''
    """смещение центра тяжести всего груза"""
    CtMovingInside = (vagon[0] / 2) - (summmnoj(gruzmass, coorctgruzx) / sum(gruzmass))
    
    """Смещение центра тяжести вместе с вагоном"""
    CtMovingWithVagon = (vagon[0] / 2) - ((summmnoj(gruzmass, coorctgruzx) + (vagon[3] * coorctvagonx)) / (sum(gruzmass) + vagon[3]))
    
    """Высота центра тяжести в вагоне"""
    CtHighGruz = (summmnoj(gruzmass, gruzz) / sum(gruzmass))
    
    """Общая высота центра тяжести"""
    CtHighAll = (summmnoj(gruzmass, gruzz) + (vagon[3] * coorctvagonz)) / (sum(gruzmass) + vagon[3])
    
    """Наветренная поверхность"""
    NavetPoverh = sum(vetst) + 7#Захардкоденно т.к. нет понимания как считается состав
    
    '''Расчёт сил на груз i'''
    '''Открыть массив с итоговыми данными'''
    for i in range(len(gruzmass)):
        '''удельная продольная инерция на одну тонну, считается для вагона'''
#        kndcq = summ(gruzmass[i])
        UdelProdInerFby1T = 1.2 - ((sum(gruzmass)) * (1.2 - 0.97)/72)
        
        '''продольная инерционная сила'''
        ProdInerF = UdelProdInerFby1T * gruzmass[i]
        
        '''поперечная инерционная сила(на 1 тонну и общая на груз)'''
        UdelPopInerFby1T = 0.33 + (0.44/vagon[6]) * abs(ctgruzx[i] - coorctvagonx)
        PopInerF = UdelPopInerFby1T * gruzmass[i]
        
        '''вертикальная инерционная сила(на 1 тонну и общая)'''
        UdelVertInerFby1T = 0.25 + 5*(10**(-6)) * (vagon[0]/2 - coorctvagonx) + 2.14/sum(gruzmass)
        VertInerF = float(UdelVertInerFby1T) * gruzmass[i]
        
        '''Ветровая нагрузка'''
        VetrNag = 50 * (10**(-3)) * vetst[i]
        
        '''Сила трения - продольная и поперечная'''
        FTrenProd = 0.5 * gruzmass[i]
        FTrenPop = 0.5 * gruzmass[i] * (1 - UdelVertInerFby1T)
        
        '''Креление должно выдержать продольно и поперечно'''
        KrepMustProd = ProdInerF - FTrenProd
        KrepMustPop = 1.25 * (PopInerF + VetrNag) - FTrenPop
        
        
        '''Устойчивость грузов'''
        '''Коэф запаса устойчивости от опрокидывания вдоль вагона'''
#        print()
        CoefZapUstOprVdol = (ctgruzx[i]) / ((ctgruzz[i]-150) * UdelProdInerFby1T)
        
        '''Коэф запаса устойчивости от опрокидывания поперёк вагона'''
#        print(gruzmass[i], pif(ctgruzy[i], ctgruzz[i]), PopInerF, ctgruzz[i]-150, VetrNag)
        CoefZapUstOprPoperek = (gruzmass[i] * pif(ctgruzx[i], ctgruzz[i])) / ((PopInerF * (ctgruzz[i]-150)) + (VetrNag * (ctgruzz[i]-150)))
        
        if (CoefZapUstOprVdol < 1.25) or (CoefZapUstOprPoperek < 1.25):
            print('Груз', i, 'устойчив менее чем 1,25')
#            print(CoefZapUstOprVdol, CoefZapUstOprPoperek)
            print(gruzx, gruzy, gruzz, gruzmass, ctgruzx, ctgruzy, ctgruzz)
            break
        else:
            print('Груз устойчив')
#            print(CoefZapUstOprVdol, CoefZapUstOprPoperek)
            print(gruzx, gruzy, gruzz, gruzmass, ctgruzx, ctgruzy, ctgruzz)
            '''1, 2, 3 - размеры по длинне, ширине, высоте; 4 - масса; 5, 6, 7 - координаты центра длинны, ширины, высоты'''

gruzx = [3650, 3870, 1080, 4100]
gruzy = [3320, 2890, 1580, 1720]
gruzz = [1500, 1020, 390, 1150]
gruzmass = [6.67, 4.085, 0.395, 1.865]
modcalc(gruzx, gruzy, gruzz, gruzmass, vagon)
