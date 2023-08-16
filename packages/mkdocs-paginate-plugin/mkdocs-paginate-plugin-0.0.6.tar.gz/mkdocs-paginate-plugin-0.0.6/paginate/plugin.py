import os
import sys
import copy
import math
import shutil
import logging

from operator import attrgetter, itemgetter

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from mkdocs.structure.nav import Section
from mkdocs.commands.build import _build_page
from mkdocs.config.config_options import Type

log = logging.getLogger(__name__)

DEBUG=os.environ.get("PAGINATE_DEBUG", False)

class PaginatePlugin(BasePlugin):

    def do_paginate(self, items, **kwargs):
        if DEBUG:
            print("------------")
            print('do_paginate')
            print(items)
            print(kwargs)
            print("NUMPAGES: ", self.num_pages)
        
        page = kwargs.get('page')

        if hasattr(page, 'page_num'):
            #pages_sorted = sorted(items, key=attrgetter(sort_key), reverse=True)
            #pages_sorted = sorted(nav.pages, key=lambda x: x.url, reverse=True)
            #chunks = [pages_sorted[i:i + max_items] for i in range(0, len(pages_sorted), max_items)]
            chunks = [items[i:i + self.max_items] for i in range(0, len(items), self.max_items)]
            if DEBUG: 
                print("NUM CHUNKS: ", len(chunks))
                print("PAGE NUM: ", (page.page_num-1))
            out_items = chunks[page.page_num-1]
        else:
            out_items = items

        return out_items

    def on_config(self, config):
        self.max_items = self.config.get('max_items', 6)

    def on_env(self, env, config, files):
        if DEBUG:
            print("----------")
            print("on_env")

        self.config = config
        env.filters['paginate'] = self.do_paginate

        self._env = env

        return env

    def create_index_file(self, homepage, pagenum, config):
        new_pagenum = pagenum
        newfile = File(
            path = homepage.file.src_path,
            src_dir = homepage.file.abs_src_path.rstrip(homepage.file.src_path),
            dest_dir = homepage.file.abs_dest_path.rstrip(homepage.file.dest_path),
            use_directory_urls = True
        )

        newfile.abs_dest_path = os.path.join(
            newfile.abs_dest_path.rstrip(newfile.dest_path),
            "page",
            str(new_pagenum),
            "index.html"
        )

        newfile.url = f"page/{new_pagenum}/"
        newpage = Page(
            title=f"page{new_pagenum}",
            file=newfile,
            config=config
        )

        # meta info will be overwritten when file is read so don't
        # attempt overrides here.
        newpage.page_num = new_pagenum
        newpage.generated = True

        return newfile


    def gen_pages(self, nav, config, files):

        for page in nav.pages:
            # Bit of a hack.  Force reading of metadata here.  This is needed
            # since we need require this info early enough in the process to
            # build out the 'nav' structure
            page.read_source(config)

        num_items = len([ x for x in nav.pages if not x.meta.get('hidden', False) ])
        self.num_pages = math.ceil(num_items/self.max_items)

        if DEBUG:
            print(f"NUM_ITEMS: {num_items}")
            print(f"NUM_PAGES: {self.num_pages}")

        homepage = next((x for x in nav.pages if x.is_homepage), None)
        homepage.page_num = 1

        # Generate pages based on number of pages we have in our nav
        # object.  
        for i in range(2, self.num_pages+1):
            # We want to start with page2, etc.
            newfile = self.create_index_file(homepage, i, config)
            newpage = newfile.page
            if i == (self.num_pages):
                newpage.last_page = True

            nav.pages.append(newpage)
            nav.items.append(newpage)
            files.append(newfile)

        if self.num_pages == 1 and homepage:
            # Homepage is the last page
            homepage.last_page = True

        return nav


    def on_nav(self, nav, config, files):
        # Build out the navigation structure

        if DEBUG: 
            print("------------")
            print("on_nav")
            print(nav)
        
        nav = self.gen_pages(nav, config, files)

        return nav
