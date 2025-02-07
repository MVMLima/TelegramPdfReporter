from typing import Dict, Optional
from templates.base_template import BaseTemplate
from templates.default_template import DefaultTemplate

class TemplateManager:
    """Manages different PDF report templates."""
    
    def __init__(self):
        self.templates: Dict[str, BaseTemplate] = {
            'default': DefaultTemplate()
        }
        self.current_template = 'default'

    def register_template(self, name: str, template: BaseTemplate) -> None:
        """Register a new template."""
        self.templates[name] = template

    def get_template(self, name: Optional[str] = None) -> BaseTemplate:
        """Get a template by name. Returns default if name not found."""
        template_name = name or self.current_template
        return self.templates.get(template_name, self.templates['default'])

    def set_default_template(self, name: str) -> bool:
        """Set the default template."""
        if name in self.templates:
            self.current_template = name
            return True
        return False

    def list_templates(self) -> Dict[str, str]:
        """List available templates with their descriptions."""
        return {name: template.__doc__ or "No description available" 
                for name, template in self.templates.items()}
