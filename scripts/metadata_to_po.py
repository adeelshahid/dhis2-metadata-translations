import os, json, polib, argparse
from dhis.config import Config
from dhis.server import Server

def get_translatable_object(api,object_name,property_name):
   props_to_get = 'id,'+ property_name
   print('Getting ' + object_name + '.' + property_name )
   return api.get(object_name,
        params={'fields': props_to_get, 'filter': str(property_name) + ':!null', 'paging': 'false'},
        return_type='collection')


def obj_to_pofile(obj,property_name):

    if (len(obj) > 0 ):
        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'translator@dhis2.org',
            'POT-Creation-Date': '2016-08-11 14:00+0100',
            'PO-Revision-Date': '2016-08-11 14:00+0100',
            'Last-Translator': 'John Traore <translator@dhis2.org>',
            'Language-Team': 'DHIS2 Development Team <post@dhis2.org>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit'}

        for props in obj:
            entry = polib.POEntry(comment=props['id'] + "." + str(property_name),msgid=props[property_name])
            po.append(entry)
        return (po)
    else:
        print("No " + property_name +  " to translate. Skipping.")


def save_obj_to_pofile(obj,file_name):
    obj.save(file_name)


def get_objs_to_translate():
    meta_objs = [{'dataElements':'name'},
                 {'dataElements':'shortName'},
                 {'organisationUnits':'name'},
                 {'organisationUnits':'shortName'},
                 {'dataSets':'name'},
                 {'dataSets' : 'shortName'},
                 {'optionSets' : 'name' },
                 {'options' : 'name'},
                 {'organisationUnitLevels': 'name'},
                 {'organisationUnitGroups' : 'name'},
                 {'organisationUnitGroups' : 'shortName'},
                 {'organisationUnitGroups' : 'description'},
                 {'organisationUnitGroupSets' : 'name'},
                 {'organisationUnitGroupSets' : 'shortName'},
                 {'organisationUnitGroupSets' : 'description'},
                 {'categoryOptions' : 'name'},
                 {'categoryOptions' : 'shortName'},
                 {'categoryOptions' : 'description'},
                 {'categories':'name'},
                 {'categories':'shortName'},
                 {'categories':'description'},
                 {'categoryCombos':'name'},
                 {'categoryOptionGroups':'name'},
                 {'categoryOptionGroups':'shortName'},
                 {'categoryOptionGroups':'description'},
                 {'categoryOptionGroupSets':'name'},
                 {'categoryOptionGroupSets':'shortName'},
                 {'categoryOptionGroupSets':'description'},
                 {'indicators':'name'},
                 {'indicators': 'shortName'},
                 {'validationRules':'name'},
                 {'programs':'name'},
                 {'programs':'shortName'},
                 {'trackedEntityAttributes':'name'},
                 {'trackedEntityAttributes':'shortName'},
                 {'programStages':'name'},
                 {'programRules':'name'},
                 {'programRules':'description'},
                 {'dataElementGroups':'name'},
                 {'dataElementGroups':'shortName'},
                 {'dataElementGroupSets':'name'},
                 {'dataElementGroupSets':'shortName'},
                 {'indicatorTypes':'name'},
                 {'indicatorGroups':'name'} ]

    return meta_objs

def parse_args():
    parser = argparse.ArgumentParser(description='Convert DHIS2 metadata to PO files')
    parser.add_argument('-s','--secrets', help='Path to the secrets file', required=True)
    args = vars(parser.parse_args())
    return args

def main():
    args = parse_args()
    local_config=os.path.abspath(args['secrets'])
    if not os.path.isfile(local_config):
        print("Warning: The credentials file "+local_config+" doesn't seem to exist, so this might not work.")
    api=Server(Config(local_config))
    meta_objs = get_objs_to_translate()

    for obj in meta_objs:
        this_object =  list( obj.keys() )[0]
        this_property = list( obj.values() )[0]
        this_obj = get_translatable_object(api, this_object, this_property)
        if  len(this_obj) > 0 :
            this_po = obj_to_pofile(this_obj, this_property)
            file_to_save = this_object + "_" + this_property + ".pot"
            if not os.path.exists("../pofiles/" + this_object):
                os.makedirs("../pofiles/" + this_object)
            this_po.save("../pofiles/" + this_object + "/" + file_to_save)
        else:
            print("No " + this_property +  " to translate for " + this_object + ".Skipping.")

if __name__ == "__main__":
    main()
