
from hashlib import md5
import re

from packages.models import Package

class Section_Parser(object):


    format_matches = (
            re.compile('^PACKAGE(\s)([\w*,\s*,\(*,\)*]*)(\:)'),
            re.compile('^([\w+,\d*,\-,\.,\(,\)]*)(\:)(\s)'),
            re.compile('^$'),
            )

    comment_match = re.compile('^(\s*)#')

    def __init__(self, section, data):
        
        self.section = section
        self.actual_checksum = md5(str(data)).hexdigest()
        self.data = data

    def _line_cleanup(self, line):

        line = line.strip().decode(unicode(self.section.repository.encoding)).strip('\n')
        
        if self.comment_match.match(line):
                return None


        for f in self.format_matches: # detecting right PACKAGES.TXT
            if f.match(line[:]):
                return line

        return None 
           
    def parse(self):
        
        if self.section.checksum == self.actual_checksum:
            return

        self.pc_checksum = self.section.make_pc_checksum() # save executes inside
        
        tmp_cache = []

        for line in self.data:
            cleaned_line = self._line_cleanup(line)
            
            if cleaned_line is None:
                continue

            if cleaned_line == '': # this is same as '^$' match
                if len(tmp_cache) > 0:
                    self.parse_package(tmp_cache)
                    tmp_cache = []
            else:
                tmp_cache.append(cleaned_line)
            
        self.section.cleanup_deprecated_packages() 
        self.section.checksum = self.actual_checksum
        self.section.save()

        Package.objects.filter(section=self.section).update(visible=True)
        
                  
    def parse_package(self, data):

        package = Package(pc_checksum=self.pc_checksum, 
                            section=self.section, 
                            distversion=self.section.distversion,
                            repository=self.section.repository,
                            visible=False
                            )

        parse_raito = {
                       'PACKAGE LOCATION': 'location',
                       'PACKAGE SIZE (compressed)': 'size_compressed',
                       'PACKAGE SIZE (uncompressed)': 'size_uncompressed',
                       'PACKAGE REQUIRED': 'requires',
                       'PACKAGE SUGGESTS': 'suggests',
                       'PACKAGE CONFLICTS': 'conflicts',
                       'PACKAGE NAME': 'raw_name',
                    }
        
        def size_item(value):

            res = re.findall('(\d+)', value)
            if len(res) <= 0:
                return 0
            else:
                return int(res[0])
        
        description = []

        for line in data:

            if self.format_matches[0].match(line[:]):
                param, value = line.split(':', 1)

                model_attr = parse_raito.get(param)
                
                if model_attr is None:
                    continue

                if param == 'PACKAGE SIZE (compressed)' or param == 'PACKAGE SIZE (uncompressed)':
                    value = size_item(value)
                try:
                    setattr(package, model_attr, value)
                except (AttributeError, ValueError), e:
                    print e 
                    return

            elif line is not None:
                description.append(line)
        
        if len(package.name) < 2: 
            return
    
        package.description = '\n'.join(description)
        
        print package.raw_name
        package.save()
        
