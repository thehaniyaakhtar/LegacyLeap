import re
import json
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from models import LegacyData, DataSourceType, FieldMapping, TableSchema

class AS400IngestionEngine:
    """Handles ingestion and parsing of various AS/400 data formats"""
    
    def __init__(self):
        self.field_patterns = {
            'numeric': r'^\d+$',
            'decimal': r'^\d+\.\d+$',
            'date': r'^\d{6,8}$|^\d{4}-\d{2}-\d{2}$',
            'time': r'^\d{6}$|^\d{2}:\d{2}:\d{2}$',
            'varchar': r'^[A-Za-z0-9\s\-_]+$'
        }
    
    def parse_flat_file(self, content: str, filename: str) -> LegacyData:
        """Parse AS/400 flat file format"""
        lines = content.strip().split('\n')
        
        # Detect fixed-width format
        if self._is_fixed_width(lines):
            return self._parse_fixed_width_file(content, filename)
        else:
            return self._parse_delimited_file(content, filename)
    
    def parse_db2_table(self, content: str, table_name: str) -> LegacyData:
        """Parse DB2 table structure from DDS or SQL"""
        if 'CREATE TABLE' in content.upper():
            return self._parse_sql_table(content, table_name)
        else:
            return self._parse_dds_file(content, table_name)
    
    def parse_green_screen(self, content: str, screen_name: str) -> LegacyData:
        """Parse green screen interface data"""
        # Extract field positions and labels
        fields = self._extract_screen_fields(content)
        
        metadata = {
            'screen_name': screen_name,
            'fields': fields,
            'field_count': len(fields)
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.GREEN_SCREEN,
            content=content,
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def parse_rpg_program(self, content: str, program_name: str) -> LegacyData:
        """Parse RPG program structure"""
        # Extract file definitions, data structures, and procedures
        file_defs = self._extract_file_definitions(content)
        data_structs = self._extract_data_structures(content)
        procedures = self._extract_procedures(content)
        
        metadata = {
            'program_name': program_name,
            'file_definitions': file_defs,
            'data_structures': data_structs,
            'procedures': procedures
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.RPG_PROGRAM,
            content=content,
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def _is_fixed_width(self, lines: List[str]) -> bool:
        """Detect if file is fixed-width format"""
        if not lines:
            return False
        
        # Check if all lines have similar length (within 10% variance)
        lengths = [len(line) for line in lines if line.strip()]
        if not lengths:
            return False
        
        avg_length = sum(lengths) / len(lengths)
        variance = sum(abs(length - avg_length) for length in lengths) / len(lengths)
        return variance < avg_length * 0.1
    
    def _parse_fixed_width_file(self, content: str, filename: str) -> LegacyData:
        """Parse fixed-width flat file"""
        lines = content.strip().split('\n')
        if not lines:
            return self._create_empty_legacy_data(filename, DataSourceType.FLAT_FILE)
        
        # Analyze column positions
        field_positions = self._detect_field_positions(lines)
        
        # Parse data into structured format
        parsed_data = []
        for line in lines:
            if line.strip():
                row = {}
                for field_name, (start, end) in field_positions.items():
                    value = line[start:end].strip()
                    row[field_name] = value
                parsed_data.append(row)
        
        metadata = {
            'filename': filename,
            'format': 'fixed_width',
            'field_positions': field_positions,
            'row_count': len(parsed_data),
            'sample_data': parsed_data[:5]  # First 5 rows as sample
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.FLAT_FILE,
            content=json.dumps(parsed_data),
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def _parse_delimited_file(self, content: str, filename: str) -> LegacyData:
        """Parse delimited flat file"""
        lines = content.strip().split('\n')
        if not lines:
            return self._create_empty_legacy_data(filename, DataSourceType.FLAT_FILE)
        
        # Detect delimiter
        delimiter = self._detect_delimiter(lines[0])
        
        # Parse CSV-like data
        parsed_data = []
        headers = lines[0].split(delimiter)
        
        for line in lines[1:]:
            if line.strip():
                values = line.split(delimiter)
                row = dict(zip(headers, values))
                parsed_data.append(row)
        
        metadata = {
            'filename': filename,
            'format': 'delimited',
            'delimiter': delimiter,
            'headers': headers,
            'row_count': len(parsed_data),
            'sample_data': parsed_data[:5]
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.FLAT_FILE,
            content=json.dumps(parsed_data),
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def _detect_delimiter(self, line: str) -> str:
        """Detect delimiter in delimited file"""
        delimiters = [',', ';', '|', '\t', ' ']
        delimiter_counts = {}
        
        for delimiter in delimiters:
            delimiter_counts[delimiter] = line.count(delimiter)
        
        return max(delimiter_counts, key=delimiter_counts.get)
    
    def _detect_field_positions(self, lines: List[str]) -> Dict[str, tuple]:
        """Detect field positions in fixed-width file"""
        if not lines:
            return {}
        
        # Use the first line as reference
        reference_line = lines[0]
        field_positions = {}
        
        # Simple heuristic: look for patterns of spaces and non-spaces
        current_pos = 0
        field_num = 1
        
        while current_pos < len(reference_line):
            # Find start of next field (non-space character)
            start = current_pos
            while start < len(reference_line) and reference_line[start].isspace():
                start += 1
            
            if start >= len(reference_line):
                break
            
            # Find end of field (space character or end of line)
            end = start
            while end < len(reference_line) and not reference_line[end].isspace():
                end += 1
            
            field_name = f"FIELD_{field_num}"
            field_positions[field_name] = (start, end)
            
            current_pos = end
            field_num += 1
        
        return field_positions
    
    def _parse_sql_table(self, content: str, table_name: str) -> LegacyData:
        """Parse SQL CREATE TABLE statement"""
        # Extract column definitions
        columns = self._extract_sql_columns(content)
        
        metadata = {
            'table_name': table_name,
            'format': 'sql',
            'columns': columns
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.DB2_TABLE,
            content=content,
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def _parse_dds_file(self, content: str, table_name: str) -> LegacyData:
        """Parse DDS (Data Description Specifications) file"""
        # Extract field definitions from DDS
        fields = self._extract_dds_fields(content)
        
        metadata = {
            'table_name': table_name,
            'format': 'dds',
            'fields': fields
        }
        
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=DataSourceType.DB2_TABLE,
            content=content,
            metadata=metadata,
            created_at=datetime.now()
        )
    
    def _extract_sql_columns(self, content: str) -> List[Dict[str, Any]]:
        """Extract column definitions from SQL"""
        columns = []
        # Simple regex to find column definitions
        pattern = r'(\w+)\s+(\w+(?:\(\d+(?:,\d+)?\))?)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        for name, data_type in matches:
            columns.append({
                'name': name,
                'type': data_type.upper(),
                'nullable': True
            })
        
        return columns
    
    def _extract_dds_fields(self, content: str) -> List[Dict[str, Any]]:
        """Extract field definitions from DDS"""
        fields = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('A') and len(line) > 10:
                # Parse DDS field definition
                field_name = line[10:20].strip()
                field_type = line[20:25].strip()
                field_length = line[25:30].strip()
                
                if field_name:
                    fields.append({
                        'name': field_name,
                        'type': field_type,
                        'length': field_length
                    })
        
        return fields
    
    def _extract_screen_fields(self, content: str) -> List[Dict[str, Any]]:
        """Extract field information from green screen"""
        fields = []
        lines = content.split('\n')
        
        for line in lines:
            # Look for field indicators (common in AS/400 screens)
            if '===' in line or '---' in line:
                continue
            
            # Extract field names and positions
            field_matches = re.findall(r'(\w+):\s*([^\s]+)', line)
            for field_name, field_value in field_matches:
                fields.append({
                    'name': field_name,
                    'value': field_value,
                    'position': line.find(field_name)
                })
        
        return fields
    
    def _extract_file_definitions(self, content: str) -> List[Dict[str, Any]]:
        """Extract file definitions from RPG program"""
        file_defs = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('F') and 'FILE' in line.upper():
                # Parse file definition
                parts = line.split()
                if len(parts) >= 2:
                    file_defs.append({
                        'name': parts[1],
                        'type': 'FILE',
                        'definition': line
                    })
        
        return file_defs
    
    def _extract_data_structures(self, content: str) -> List[Dict[str, Any]]:
        """Extract data structures from RPG program"""
        data_structs = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('D') and 'DS' in line.upper():
                # Parse data structure definition
                parts = line.split()
                if len(parts) >= 2:
                    data_structs.append({
                        'name': parts[1],
                        'type': 'DS',
                        'definition': line
                    })
        
        return data_structs
    
    def _extract_procedures(self, content: str) -> List[Dict[str, Any]]:
        """Extract procedures from RPG program"""
        procedures = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('C') and 'BEGSR' in line.upper():
                # Parse procedure start
                parts = line.split()
                if len(parts) >= 2:
                    procedures.append({
                        'name': parts[1],
                        'type': 'PROCEDURE',
                        'definition': line
                    })
        
        return procedures
    
    def _create_empty_legacy_data(self, filename: str, source_type: DataSourceType) -> LegacyData:
        """Create empty legacy data for empty files"""
        return LegacyData(
            id=str(uuid.uuid4()),
            source_type=source_type,
            content="",
            metadata={'filename': filename, 'empty': True},
            created_at=datetime.now()
        )
