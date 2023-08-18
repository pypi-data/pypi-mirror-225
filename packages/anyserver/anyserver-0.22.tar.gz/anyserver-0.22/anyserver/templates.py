#!/usr/bin/env python3
import os
import sys
import argparse
import logging

from glob import glob
from string import Template

from anyserver.encoders import DEFAULT_ENCODERS, fromFile
from anyserver.router import WebRouter

logger = logging.getLogger('templates')


class TemplateEngine:
    mappings = {}   # <-- Track valid file extensions for each mime type
    templates = {}  # <-- Maintain a list of template paths and renderers per path
    renderer = None

    def __init__(self, path='./templates', default='application/json', encoders=DEFAULT_ENCODERS, renderer=None):
        self.base = path
        self.default = default
        self.encoders = encoders
        self.renderer = renderer
        self.templates = {}

        # Register the default set of encoders that will be used to format response types
        for enc in encoders:
            self.encoder(enc.mime, enc.ext, enc.encode)

    def encoder(self, mime_type, file_types, render_template):
        self.register("*", mime_type, render_template, file_types)

    def register(self, path, ctype, render_template, ext=[]):
        # Register the rendererers for the specified path and content type
        templates = self.templates
        templates[path] = templates[path] if path in templates else {}
        templates[path][ctype] = render_template

        if len(ext):
            # Add mappings (if specified) to list of known file extensions
            mappings = self.mappings
            mappings[ctype] = mappings[ctype] if ctype in mappings else []
            mappings[ctype] = list(set(mappings[ctype] + ext))

    def find(self, path, ctype=None):
        templates = self.templates
        logger.debug('FIND[%s] (ctype: %s)' % (path, ctype))

        # If no content type specified, we will search for available response types
        if path in templates and not ctype and len(list(templates[path].keys())):
            # Return the default content type, or the first available type (if no default set)
            default = self.default
            ctype = default if default in templates[path] else list(
                templates[path].keys())[0]
            logger.debug('GETS[%s] (ctype: %s)' % (path, ctype))
        else:
            # Fall back to default content type (if not specified)
            ctype = self.default if not ctype else ctype

        # Get the render template by path and content type
        if path in templates and ctype in templates[path]:
            return templates[path][ctype]

        # Get the default renderer for this content type
        if '*' in templates and ctype in templates['*']:
            return templates['*'][ctype]

        # No render engine found for content type
        return None

    def render(self, path, data, ctype=None):
        template = self.find(path, ctype)
        logger.debug('TMPL[%s] = %s' % (path, template))
        if template:
            # Render the result using a template
            logger.debug('DATA[%s] = %s' % (path, data))
            return template(data)
        else:
            # No template engine found to render with
            return ""

    def load(self, path, ctype=None):
        templates = self.templates
        templates[path] = templates[path] if path in templates else {}
        logger.debug('LOAD[%s] (ctype: %s)' % (path, ctype))

        # Search for known file types (or the given mine type)
        types = [ctype] if ctype else self.mappings.keys()
        for type in types:
            found = self.discover(path, type)
            if found:
                logger.debug('LOAD[%s] (ctype: %s) <=- %s' %
                             (path, type, found))
                templates[path][type] = self.bind(path, type, found)

    def bind(self, path, ctype, filename):
        def default_render(data):
            # Use the built-in python template engine by default
            with open(filename, 'r') as file:
                content = file.read()
                template = Template(content)
                return template.substitute(data)

        def render_template(data, resp=None):
            if resp and ctype:
                # Update the response's content type header
                resp.head['content-type'] = ctype

            if self.renderer:
                # Render the template given the render engine
                return self.renderer(filename, data)
            else:
                # Use the built in python template engine
                return default_render(data)

        return render_template

    def discover(self, path, ctype=None):

        # Check if template for content type is cached
        if ctype and ctype in self.templates[path]:
            return self.templates[path][ctype]

        # Define the file path prefix (excl. extensions)
        path = path if not path.startswith("/") else path[1:]
        target = os.path.join(self.base, path)

        # Try and search the filesystem for mappings to the file types
        if ctype in self.mappings:
            # Find the extensions for the given mime type
            mappings = self.mappings[ctype]
            files = []
            for ext in set(mappings):
                files.extend(glob(target+"*"+ext))
            if len(files):
                found = files[0]  # Return first matched file template
                return found

        # Fallback, if the file target exists (no extended prefixes),
        # load it explicitly as the template.
        if os.path.isfile(target):
            return target


class TemplateRouter(WebRouter):
    cache = {}

    def __init__(self, prefix='', render=None, routes=None):
        super().__init__(prefix, routes)
        self.templates = TemplateEngine(renderer=render)

    def renders(self, path, content_type=''):
        def decorator(action):
            # Save a ref for this action to be linked to the render template path
            self.cache[action] = path
            self.templates.load(path, content_type)
            return action
        return decorator

    def format(self, action):
        # Transform the base result into a templated and formatted response
        def formatted(req, resp):
            data = action(req, resp)

            # Now that we have a valid response, try to render and encode the result
            ctype = resp.head['content-type'] if 'content-type' in resp.head else ''
            if not action in self.cache:
                # No template is associated with this action, return encoded respionse
                return self.templates.render('*', data, ctype)

            # Render the result using the current template engine
            path = self.cache[action]
            return self.templates.render(path, data, ctype)

        return formatted

