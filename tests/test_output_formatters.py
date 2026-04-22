import pytest
import json
import csv
import os
from unittest.mock import patch, Mock, mock_open

from models.crypto_asset import CryptoAsset
from formatters.console import ConsoleFormatter
from formatters.json import JSONFormatter
from formatters.csv import CSVFormatter
from formatters.factory import FormatterFactory
from formatters.base import OutputFormatter


class TestConsoleFormatter:
    """Тесты для ConsoleFormatter"""
    
    def test_console_formatter_inherits_from_base(self):
        """ConsoleFormatter наследуется от OutputFormatter"""
        formatter = ConsoleFormatter()
        assert isinstance(formatter, OutputFormatter)
    
    def test_format_prints_each_asset(self, sample_assets_list):
        """format печатает каждый актив через print"""
        formatter = ConsoleFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format(sample_assets_list)
        
        # Проверяем что print вызван для каждого актива
        assert mock_print.call_count == len(sample_assets_list)
        
        # Проверяем что передавались правильные объекты
        for i, asset in enumerate(sample_assets_list):
            assert mock_print.call_args_list[i][0][0] == asset
    
    def test_format_empty_list(self):
        """format с пустым списком не печатает ничего"""
        formatter = ConsoleFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format([])
        
        mock_print.assert_not_called()
    
    def test_format_single_asset(self, sample_asset):
        """format с одним активом"""
        formatter = ConsoleFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format([sample_asset])
        
        mock_print.assert_called_once_with(sample_asset)


class TestJSONFormatter:
    """Тесты для JSONFormatter"""
    
    def test_json_formatter_inherits_from_base(self):
        """JSONFormatter наследуется от OutputFormatter"""
        formatter = JSONFormatter()
        assert isinstance(formatter, OutputFormatter)
    
    def test_format_outputs_valid_json(self, sample_assets_list):
        """format выводит валидный JSON"""
        formatter = JSONFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format(sample_assets_list)
        
        # Проверяем что print вызван один раз
        assert mock_print.call_count == 1
        
        # Получаем вывод и парсим JSON
        output = mock_print.call_args[0][0]
        data = json.loads(output)
        
        # Проверяем структуру
        assert isinstance(data, list)
        assert len(data) == len(sample_assets_list)
        
        # Проверяем данные первого актива
        assert data[0]["name"] == sample_assets_list[0].name
        assert data[0]["symbol"] == sample_assets_list[0].symbol
        assert data[0]["price"] == sample_assets_list[0].price
        assert data[0]["change_24h"] == sample_assets_list[0].change_24h
    
    def test_format_empty_list(self):
        """format с пустым списком выводит пустой JSON массив"""
        formatter = JSONFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format([])
        
        output = mock_print.call_args[0][0]
        data = json.loads(output)
        assert data == []
    
    def test_format_json_indent(self, sample_asset):
        """JSON форматируется с отступом indent=2"""
        formatter = JSONFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format([sample_asset])
        
        output = mock_print.call_args[0][0]
        # Проверяем что есть переносы строк (признак форматирования с indent)
        assert "\n" in output
        assert '  "' in output  # два пробела перед ключом
    
    @pytest.mark.parametrize("assets_count", [0, 1, 3, 10])
    def test_format_various_counts(self, assets_count):
        """Параметризованный тест с разным количеством активов"""
        assets = [
            CryptoAsset(f"Coin{i}", f"C{i}", 1.0 * i, 0.1 * i)
            for i in range(assets_count)
        ]
        
        formatter = JSONFormatter()
        
        with patch("builtins.print") as mock_print:
            formatter.format(assets)
        
        output = mock_print.call_args[0][0]
        data = json.loads(output)
        assert len(data) == assets_count


class TestCSVFormatter:
    """Тесты для CSVFormatter"""
    
    def test_csv_formatter_inherits_from_base(self):
        """CSVFormatter наследуется от OutputFormatter"""
        formatter = CSVFormatter()
        assert isinstance(formatter, OutputFormatter)
    
    def test_format_writes_csv_file(self, sample_assets_list):
        """format записывает данные в CSV файл"""
        formatter = CSVFormatter()
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            formatter.format(sample_assets_list)
        
        # Проверяем что файл открыт для записи
        mock_file.assert_called_once_with("output.csv", "w", newline="")
        
        # Получаем все записи
        handle = mock_file()
        writer_calls = handle.write.call_args_list
        
        # Проверяем что были записи (хотя бы заголовок)
        assert len(writer_calls) > 0
    
    def test_format_writes_correct_headers(self, sample_asset):
        """CSV содержит правильные заголовки"""
        formatter = CSVFormatter()
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("csv.writer") as mock_writer:
                mock_writer_instance = Mock()
                mock_writer.return_value = mock_writer_instance
                
                formatter.format([sample_asset])
        
        # Проверяем вызов writerow для заголовков
        header_call = mock_writer_instance.writerow.call_args_list[0]
        assert header_call[0][0] == ["name", "symbol", "price", "change_24h"]
    
    def test_format_writes_correct_data(self, sample_asset):
        """CSV содержит правильные данные активов"""
        formatter = CSVFormatter()
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("csv.writer") as mock_writer:
                mock_writer_instance = Mock()
                mock_writer.return_value = mock_writer_instance
                
                formatter.format([sample_asset])
        
        # Второй вызов - данные актива
        data_call = mock_writer_instance.writerow.call_args_list[1]
        expected_row = [
            sample_asset.name,
            sample_asset.symbol,
            sample_asset.price,
            sample_asset.change_24h
        ]
        assert data_call[0][0] == expected_row
    
    def test_format_empty_list(self):
        """format с пустым списком записывает только заголовки"""
        formatter = CSVFormatter()
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("csv.writer") as mock_writer:
                mock_writer_instance = Mock()
                mock_writer.return_value = mock_writer_instance
                
                formatter.format([])
        
        # Только один вызов - заголовки
        assert mock_writer_instance.writerow.call_count == 1
    
    def test_format_creates_output_csv_file(self, sample_assets_list, tmp_path):
        """Интеграционный тест - реальное создание CSV файла"""
        # Используем временную директорию
        csv_path = tmp_path / "output.csv"
        
        # Патчим open чтобы писать в tmp_path
        original_open = open
        
        def mock_open_wrapper(*args, **kwargs):
            if args[0] == "output.csv":
                return original_open(csv_path, *args[1:], **kwargs)
            return original_open(*args, **kwargs)
        
        formatter = CSVFormatter()
        
        with patch("builtins.open", side_effect=mock_open_wrapper):
            formatter.format(sample_assets_list)
        
        # Проверяем что файл создан
        assert csv_path.exists()
        
        # Читаем и проверяем содержимое
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        assert rows[0] == ["name", "symbol", "price", "change_24h"]
        assert len(rows) == 1 + len(sample_assets_list)


class TestFormatterFactory:
    """Тесты для FormatterFactory"""
    
    def test_create_console_formatter(self):
        """Фабрика создаёт ConsoleFormatter"""
        formatter = FormatterFactory.create("console")
        assert isinstance(formatter, ConsoleFormatter)
    
    def test_create_json_formatter(self):
        """Фабрика создаёт JSONFormatter"""
        formatter = FormatterFactory.create("json")
        assert isinstance(formatter, JSONFormatter)
    
    def test_create_csv_formatter(self):
        """Фабрика создаёт CSVFormatter"""
        formatter = FormatterFactory.create("csv")
        assert isinstance(formatter, CSVFormatter)
    
    def test_create_unknown_formatter_raises_error(self):
        """Создание неизвестного форматтера вызывает ValueError"""
        with pytest.raises(ValueError, match="Unknown formatter"):
            FormatterFactory.create("xml")
    
    @pytest.mark.parametrize("name,expected_class", [
        ("console", ConsoleFormatter),
        ("json", JSONFormatter),
        ("csv", CSVFormatter),
    ])
    def test_factory_parametrized(self, name, expected_class):
        """Параметризованный тест фабрики"""
        formatter = FormatterFactory.create(name)
        assert isinstance(formatter, expected_class)
    
    def test_factory_returns_output_formatter(self):
        """Все созданные объекты наследуются от OutputFormatter"""
        for name in ["console", "json", "csv"]:
            formatter = FormatterFactory.create(name)
            assert isinstance(formatter, OutputFormatter)


class TestFormatterPolymorphism:
    """Тесты полиморфизма форматтеров"""
    
    def test_all_formatters_implement_format(self):
        """Все форматтеры реализуют метод format"""
        formatters = [
            ConsoleFormatter(),
            JSONFormatter(),
            CSVFormatter()
        ]
        
        for formatter in formatters:
            assert hasattr(formatter, "format")
            assert callable(formatter.format)
    
    def test_formatters_accept_same_input(self, sample_assets_list):
        """Все форматтеры принимают одинаковый входной формат"""
        formatters = [
            ConsoleFormatter(),
            JSONFormatter(),
            CSVFormatter()
        ]
        
        for formatter in formatters:
            # Не должно быть исключений
            try:
                if isinstance(formatter, CSVFormatter):
                    mock_file = mock_open()
                    with patch("builtins.open", mock_file):
                        formatter.format(sample_assets_list)
                elif isinstance(formatter, JSONFormatter):
                    with patch("builtins.print"):
                        formatter.format(sample_assets_list)
                else:
                    with patch("builtins.print"):
                        formatter.format(sample_assets_list)
            except Exception as e:
                pytest.fail(f"{formatter.__class__.__name__}.format raised {e}")
    
    def test_liskov_substitution(self, sample_assets_list):
        """LSP - можно подменить любой форматтер"""
        
        def output_with_formatter(formatter: OutputFormatter, assets):
            """Функция работает с любым форматтером"""
            if isinstance(formatter, CSVFormatter):
                mock_file = mock_open()
                with patch("builtins.open", mock_file):
                    formatter.format(assets)
            else:
                with patch("builtins.print"):
                    formatter.format(assets)
        
        # Должно работать со всеми
        output_with_formatter(ConsoleFormatter(), sample_assets_list)
        output_with_formatter(JSONFormatter(), sample_assets_list)
        output_with_formatter(CSVFormatter(), sample_assets_list)