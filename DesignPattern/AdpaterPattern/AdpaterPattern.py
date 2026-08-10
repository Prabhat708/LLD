from abc import ABC, abstractmethod


# 1. Target interface expected by the client
class IReports(ABC):

    # now takes the raw data string and returns JSON
    @abstractmethod
    def get_json_data(self, data):
        pass


# 2. Adaptee: provides XML data from a raw input
class XmlDataProvider:

    # Expect data in "name:id" format (e.g. "Alice:42")
    def get_xml_data(self, data):

        separator = data.find(":")

        name = data[:separator]
        user_id = data[separator + 1:]

        # Build an XML representation
        return (
            "<user>"
            "<name>" + name + "</name>"
            "<id>" + user_id + "</id>"
            "</user>"
        )


# 3. Adapter: implements IReports by converting XML → JSON
class XmlDataProviderAdapter(IReports):

    def __init__(self, provider):
        self.xml_provider = provider

    def get_json_data(self, data):

        # 1. Get XML from the adaptee
        xml = self.xml_provider.get_xml_data(data)

        # 2. Naïvely parse out <name> and <id> values
        start_name = xml.find("<name>") + 6
        end_name = xml.find("</name>")

        name = xml[start_name:end_name]

        start_id = xml.find("<id>") + 4
        end_id = xml.find("</id>")

        user_id = xml[start_id:end_id]

        # 3. Build and return JSON
        return f'{{"name":"{name}", "id":{user_id}}}'


# 4. Client code works only with IReports
class Client:

    def get_report(self, report, raw_data):
        print(
            "Processed JSON:",
            report.get_json_data(raw_data)
        )


def main():

    # 1. Create the adaptee
    xml_prov = XmlDataProvider()

    # 2. Make our adapter
    adapter = XmlDataProviderAdapter(xml_prov)

    # 3. Give it some raw data
    raw_data = "Alice:42"

    # 4. Client prints the JSON
    client = Client()
    client.get_report(adapter, raw_data)

    # → Processed JSON: {"name":"Alice", "id":42}

    # 5. Cleanup
    # Python handles memory cleanup automatically.


if __name__ == "__main__":
    main()