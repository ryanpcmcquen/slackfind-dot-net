
from urllib import urlopen

from packages.models import SubRepository

def download_section_metadata(section):

    f = urlopen(section.get_absolute_url()+'PACKAGES.TXT')
    
    result = f.readlines()
    print len(result)
    f.close()

    for subrepository in SubRepository.objects.filter(repository=section.repository):

        f = urlopen(section.get_absolute_url() + subrepository.path + 'PACKAGES.TXT')
        result += f.readlines()
        f.close()

    return result


