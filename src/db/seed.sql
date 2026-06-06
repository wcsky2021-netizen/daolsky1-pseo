-- daolsky1-pseo seed (다올스카이차 / daolsky1.co.kr)
-- 형님 사이트 전용. 기존 아자스카이(아자스카이/wormsz1) 데이터와 완전 분리.
--
-- ⚠️ phone 은 형님 실제 대표번호로 교체 필요 (아래 TODO).
-- naver_verification 은 네이버 서치어드바이저에 daolsky1.co.kr 등록 후 발급코드로 UPDATE.
--   UPDATE sites SET naver_verification='<코드>' WHERE domain='daolsky1.co.kr';

INSERT OR IGNORE INTO sites (id, domain, site_name, phone) VALUES
  (1, 'daolsky1.co.kr', '다올스카이차', 'TODO_형님_대표번호');

INSERT OR IGNORE INTO boards (site_id, slug, title, display_order) VALUES
  (1, '스카이차',         '스카이차',         1),
  (1, '스카이차-일대',     '스카이차 일대',     2),
  (1, '스카이-작업차',     '스카이 작업차',     3),
  (1, '스카이차-요금',     '스카이차 요금',     4),
  (1, '스카이차-비용',     '스카이차 비용',     5),
  (1, '스카이차-가격',     '스카이차 가격',     6),
  (1, '스카이차-이용료',   '스카이차 이용료',   7),
  (1, '고소작업차량',      '고소작업차량',      8);
