from Model import Model,Measurement,filt_design_type
import pandas as pd

def get_filtered_list(filters,model):
    try:
        return [m for m in model.saved_measurements if all(f(m) for f in filters)]
    except TypeError: # Likely not passed as list, but as a single filter class instead.
        return [m for m in model.saved_measurements if filters(m)]

def change_value(filters, propertyname,value):
    model = Model()
    model.load()

    measurements = get_filtered_list(filters,model)
    for m in measurements:
        if propertyname in m.__dict__:
            setattr(m, propertyname, value)
        else:
            m[propertyname] = value

    model.save()

def change_waferID(filters, old,new):
    model = Model()
    model.load()
    measurements = get_filtered_list(filters,model)
    for m in measurements:
        s = m.sampleID
        m.sampleID = s.replace(old,new)

    model.save()

def delete_property(filters,propertyname):
    model = Model()
    model.load()
    measurements = get_filtered_list(filters,model)

    for m in measurements:
        m.delete_property(propertyname)

    model.save()


def add_property(filters, propertyname,value,unit=''):
    model = Model()
    model.load()
    measurements = get_filtered_list(filters, model)

    for m in measurements:
        m.add_property(propertyname,value,unit)

    model.save()


def update_TOT_data():
    model = Model()
    model.load()

    # Correct design type name
    filt = filt_design_type('Toplogy Optimized Trampoline')
    measurements = [m for m in model.saved_measurements if filt(m)]
    for m in measurements:
        m.design_type = 'Topology Optimized Trampoline'

    # Find topology optimized trampolines
    filt = filt_design_type('Topology Optimized Trampoline')
    measurements = [m for m in model.saved_measurements if filt(m)]

    # Load list of legacy data
    df = pd.read_excel("Old list of samples.xlsx",
                       "Toplogy Optimized Trampoline",
                       skiprows = 1)
    df2 = pd.read_excel("samples.xlsx")

    # Update data
    unknowns = 0
    total = 0
    for m in measurements:
        total += 1
        row = df2.loc[df2['sampleID'] == m.sampleID]
        found = True
        if len(row):
            design = row['designID'].values[0]
        else:
            row = df.loc[df['sample ID'] == m.sampleID]
            if len(row):
                design = row['design ID'].values[0]
            else:
                row = []
                design = None
        if len(row):
            if ("D1" in design) or design == "Design1":
                design = "D1"
            elif design == "Design1Var":
                design = "D1A"
            elif ("D2" in design) or design == "Design2":
                design = "D2"
            elif ("D3" in design) or design == "Design3":
                design = "D3"
            elif ("D4" in design) or design == "Design4":
                design = "D4"
            elif ("D5" in design) or design == "Design5":
                design = "D5"
        elif "TOT115" in m.sampleID:
            waferpos = m.sampleID[-2:]
            if waferpos in ["21","51","12","42","72","23","53","83","34","64","15","45","75","26","56","86","37","67","28","58"]:
                design = "D1"
            elif waferpos in ["31","61","22","52","82","33","63","14","44","74","25","55","85","36","66","17","47","77","38","68"]:
                design = "D2"
            elif waferpos in ["41","71","32","62","13","43","73","24","54","84","35","65","16","46","76","27","57","87","48","78"]:
                design = "D3"
            else:
                raise Exception()
        else:
            #raise Exception()
            found = False
            unknowns += 1
            print(m.sampleID)
        if found:
            m.add_property('design', design)
            #print(m.sampleID,m['design'])
        else:
            m.add_property('design', '')
    print("Unknowns =", unknowns)
    print("Total =", total)

    # Save
    model.save()

update_TOT_data()
#Toplogy Optimized Trampoline