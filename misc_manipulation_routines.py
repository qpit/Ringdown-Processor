from Model import Model,Measurement

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







# change_waferID([filt_sampleID('DP206'),
#                                     filt_property('Lp',100,'<')],
#                                     'DP206','DP209')

# for waferID in ['DP206','DP207','DP196']:
#     change_value([filt_sampleID(waferID)],
#                  'Lp',221)

# for p in ['h_pil','d_pil']:
#     try:
#         delete_property([],p)
#     except ValueError:
#         pass

add_property(filt_design_type('Density Phononic Membrane'),'g',5)


