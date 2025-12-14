import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime


class QiitaAPIClient:
    BASE_URL = "https://qiita.com/api/v2"
    
    def __init__(self, access_token: Optional[str] = None, timeout: int = 30):
        self.access_token = access_token
        self.timeout = timeout
        self.headers = self._build_headers()
    
    def _build_headers(self) -> Dict[str, str]:
        """認証ヘッダーを構築"""
        headers = {"Accept": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    def get_items(
        self, 
        page: int = 1, 
        per_page: int = 20,
        query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/items"
        params = {
            "page": page,
            "per_page": min(per_page, 100),  # 最大100まで
        }
        
        if query:
            params["query"] = query
        
        return self._get_request(url, params)
    
    def _get_request(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def _async_get_request(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def format_items_for_email(items: List[Dict[str, Any]]) -> str:
        if not items:
            return "取得できる記事がありません。"
        
        formatted_text = ""
        
        for i, item in enumerate(items, 1):
            # 日時フォーマット
            created_at = QiitaAPIClient._format_datetime(item.get("created_at"))
            
            # タグ情報
            tags = item.get("tags", [])
            tags_str = ", ".join([tag["name"] for tag in tags]) if tags else "なし"
            
            # 記事情報
            section = f"""■ {i}. {item.get('title', 'タイトルなし')}

【著者】{item.get('user', {}).get('name', '不明')}
【公開日】{created_at}
【タグ】{tags_str}
【URL】{item.get('url', 'URLなし')}

【統計情報】
  👍 いいね: {item.get('likes_count', 0)}
  💬 コメント: {item.get('comments_count', 0)}
  ⭐ ストック: {item.get('stocks_count', 0)}
  👀 ページビュー: {item.get('page_views_count', 0)}
  😊 リアクション: {item.get('reactions_count', 0)}

"""
            formatted_text += section
        
        return formatted_text
    
    @staticmethod
    def _format_datetime(datetime_str: Optional[str]) -> str:
        if not datetime_str:
            return "不明"
        
        try:
            # ISO 8601形式をパース
            dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
            # 見やすい形式に変換
            return dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            return datetime_str
    


if __name__ == "__main__":
    # 使用例
    client = QiitaAPIClient()
    items = client.get_items(per_page=10, query="LLM")
    
    # メール用に整形
    email_content = QiitaAPIClient.format_items_for_email(items)
